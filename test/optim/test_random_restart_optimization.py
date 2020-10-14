#! /usr/bin/env python3

import torch
from botorch.acquisition import qExpectedImprovement
from botorch.gen import gen_candidates_scipy, get_best_candidates

from ..test_gen import TestBaseCandidateGeneration


class TestRandomRestartOptimization(TestBaseCandidateGeneration):
    def test_random_restart_optimization(self, cuda=False):
        for double in (True, False):
            self._setUp(double=double, cuda=cuda)
            best_f = self.model(self.train_x).mean.max().item()
            qEI = qExpectedImprovement(self.model, best_f=best_f)
            bounds = torch.tensor([[0.0], [1.0]]).type_as(self.train_x)
            batch_ics = torch.rand(2, 1).type_as(self.train_x)
            batch_candidates, batch_acq_values = gen_candidates_scipy(
                initial_candidates=batch_ics,
                acquisition_function=qEI,
                lower_bounds=bounds[0],
                upper_bounds=bounds[1],
                options={"maxiter": 3},
            )
            candidates = get_best_candidates(
                batch_candidates=batch_candidates, batch_values=batch_acq_values
            )            
            self.assertTrue(0 <= candidates)
            self.assertTrue(candidates <= 1)

    def test_random_restart_optimization_cuda(self):
        if torch.cuda.is_available():
            self.test_random_restart_optimization(cuda=True)
