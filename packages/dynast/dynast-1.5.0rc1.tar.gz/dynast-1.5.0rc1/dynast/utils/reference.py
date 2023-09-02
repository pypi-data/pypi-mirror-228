# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
import os
from typing import Tuple

import torch
import torchvision
import torchvision.models as models
from neural_compressor import PostTrainingQuantConfig, quantization
from torch import nn

from dynast.utils import log, measure_time, set_logger
from dynast.utils.datasets import Dataset, ImageNet
from dynast.utils.nn import get_macs, get_parameters, measure_latency, validate_classification


def get_torchvision_model(
    model_name: str,
    quantized: bool = False,
    progress: bool = False,
) -> nn.Module:
    try:
        if not quantized:
            model = getattr(models, model_name)(pretrained=True, progress=progress)
        else:
            model = getattr(models.quantization, model_name)(pretrained=True, quantize=quantized, progress=progress)
        model.eval()
        return model
    except AttributeError as ae:
        log.error(
            'Model {model_name} not available. This can be due to either a typo or the model is not '
            'available in torchvision=={torchvision_version}. \nAvailable models: {available_models}'.format(
                model_name=model_name,
                torchvision_version=torchvision.__version__,
                available_models=', '.join([m for m in dir(models) if not m.startswith('_')]),
            )
        )
        raise ae


class Reference(object):
    @measure_time
    def validate(
        self,
        device: str = 'cpu',
        batch_size: int = 128,
        input_size: int = 224,
        test_size: int = None,
    ):
        raise NotImplementedError()

    @measure_time
    def benchmark(
        self,
        device: str = 'cpu',
        batch_size: int = 128,
        input_size: int = 224,
        warmup_steps: int = 10,
        measure_steps: int = 50,
    ):
        raise NotImplementedError()


class TorchVisionReference(Reference):
    def __init__(
        self,
        model_name: str,
        model_path: str = None,
        dataset: Dataset = ImageNet,
        dataset_path: str = None,
        quantized: bool = False,
    ) -> None:
        self.model_name = model_name
        self.dataset = dataset
        self.quantized = quantized

        if dataset_path:
            self.dataset.PATH = dataset_path

        log.info(
            '{name} for \'{model_name}\' on \'{dataset_name}\' dataset'.format(
                name=str(self),
                model_name=self.model_name,
                dataset_name=self.dataset.name(),
            )
        )

        if model_path and os.path.exists(model_path):
            log.info(f'Loading model from {model_path}')
            self.model = torch.load(model_path)
        else:
            self.model = get_torchvision_model(model_name=self.model_name, quantized=self.quantized)
            if model_path:
                log.info(f'Loading model from {model_path} failed - model does not exists. Downloading and saving...')
                torch.save(self.model, model_path)

        self.model.eval()

    @measure_time
    def validate(
        self,
        device: str = 'cpu',
        batch_size: int = 128,
        input_size: int = 224,
        test_fraction: float = 1.0,
    ) -> Tuple[float, float, float]:
        model = self.model.to(device)
        loss, top1, top5 = validate_classification(
            model=model,
            device=device,
            data_loader=self.dataset.validation_dataloader(
                batch_size=batch_size,
                image_size=input_size,
                fraction=test_fraction,
            ),
        )
        log.info(
            '\'{model_name}\' on \'{dataset_name}\' - top1 {top1} top5 {top5} loss {loss}'.format(
                model_name=self.model_name,
                dataset_name=self.dataset.name(),
                top1=top1,
                top5=top5,
                loss=loss,
            )
        )
        return loss, top1, top5

    @measure_time
    def benchmark(
        self,
        device: str = 'cpu',
        batch_size: int = 128,
        input_size: int = 224,
        warmup_steps: int = 10,
        measure_steps: int = 50,
    ) -> Tuple[float, float]:
        model = self.model.to(device)
        latency_mean, latency_std = measure_latency(
            model=model,
            input_size=(batch_size, 3, input_size, input_size),
            warmup_steps=warmup_steps,
            measure_steps=measure_steps,
            device=device,
        )
        log.info(
            '\'{model_name}\' (BS={batch_size}) mean latency {latency_mean} +/- {latency_std}'.format(
                model_name=self.model_name,
                batch_size=batch_size,
                latency_mean=latency_mean,
                latency_std=latency_std,
            )
        )
        return latency_mean, latency_std

    @measure_time
    def get_gflops(
        self,
        device: str = 'cpu',
        input_size: int = 224,
    ):
        return get_macs(
            model=self.model,
            input_size=(1, 3, input_size, input_size),
            device=device,
        )

    @measure_time
    def get_params(self):
        return get_parameters(model=self.model)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model', type=str, required=True)
    parser.add_argument('--model_path', type=str, default=None)
    parser.add_argument('-b', '--batch_size', type=int, default=128)
    parser.add_argument(
        '--test_fraction', type=float, default=1.0, help='Fraction of dataset to be used for validation.'
    )
    parser.add_argument('--dataset_path', default=None, type=str, help='')
    parser.add_argument(
        '--warmup_steps',
        type=int,
        default=10,
        help='How many batches should be used to warm up latency measurement when benchmarking.',
    )
    parser.add_argument(
        '--measure_steps',
        type=int,
        default=100,
        help='How many batches should be used for actual latency measurement when benchmarking.',
    )
    parser.add_argument('--device', type=str, choices=['cpu', 'cuda'], default='cpu')
    parser.add_argument('--dataset', type=str, choices=['imagenet', 'imagenette', 'cifar10'], default='imagenet')
    parser.add_argument('--input_size', type=int, default=224)
    parser.add_argument('-d', '--debug', action='store_true')

    args = parser.parse_args()

    if args.debug:
        set_logger(logging.DEBUG)

    log.info('Settings: {}'.format(args))

    ref = TorchVisionReference(
        model_name=args.model,
        model_path=args.model_path,
        dataset=Dataset.get(args.dataset),
        dataset_path=args.dataset_path,
        quantized=False,
    )

    train_loader = ref.dataset.train_dataloader(batch_size=args.batch_size, image_size=args.input_size, shuffle=False)
    val_loader = ref.dataset.validation_dataloader(
        batch_size=args.batch_size, image_size=args.input_size, shuffle=False, fraction=0.05
    )

    conf = PostTrainingQuantConfig()
    q_model = quantization.fit(
        ref.model,
        conf,
        calib_dataloader=train_loader,
    )

    # top1 = validate_classification(q_model, data_loader=val_loader)[1]
    # lat = measure_latency(q_model, (args.batch_size, 3, args.input_size, args.input_size), device=args.device)
    # print(f'{args.model} top1: {top1} lat: {lat}')

    ref.validate(
        device=args.device,
        batch_size=args.batch_size,
        test_fraction=args.test_fraction,
    )
    ref.benchmark(
        device=args.device,
        batch_size=args.batch_size,
        input_size=args.input_size,
        warmup_steps=args.warmup_steps,
        measure_steps=args.measure_steps,
    )

    ref.model = q_model
    ref.validate(
        device=args.device,
        batch_size=args.batch_size,
        test_fraction=args.test_fraction,
    )
    ref.benchmark(
        device=args.device,
        batch_size=args.batch_size,
        input_size=args.input_size,
        warmup_steps=args.warmup_steps,
        measure_steps=args.measure_steps,
    )
