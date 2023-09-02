from remin.solver import Solver, make_trainer
from remin.residual import Residual, make_loader
from remin.solver.residual_loss import FuncLoss
from remin import func, domain, callbacks
import torch
import numpy as np
from torch import nn
from model import Shrodinger

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.set_default_device(device)
torch.set_float32_matmul_precision('high')
torch.manual_seed(0)
np.random.seed(0)

omega = 0.5
E = 2.75

model = Shrodinger()
U = func.functional_call(model)
dU = func.fgrad(U)
ddU = func.fgrad(dU)

def de_residual(params, x):
    V = 0.5 * omega**2 * x**2
    return -0.5*ddU(params, x) + (V - E) * U(params, x),

def ic1_residual(params, x):
    return U(params, x), dU(params, x) - 0.86


de_col = domain.Line((-10,), (10,), 100)
ic_col = domain.Point((0,))

de_res = Residual(de_col, de_residual)
ic_res = Residual(ic_col, ic1_residual)

if __name__ == '__main__':
    
    loader = make_loader(
        [de_res, ic_res],
        fully_loaded=True
    )

    epochs = 20000
    lr = 5e-3

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    resloss = FuncLoss(nn.MSELoss())
    metloss = FuncLoss(nn.HuberLoss())
    trainer = make_trainer(loader,
                           optimizer=optimizer,
                           residual_loss=resloss,
                           metric_loss=metloss)
    
    solver = Solver(model,
                    'schrodinger_func',
                    'outputs',
                    trainer=trainer)
    solver.reset_callbacks(
        callbacks.TotalTimeCallback(),
        callbacks.SaveCallback(),
        callbacks.LogCallback(log_epoch=1000, log_progress=100),
        callbacks.PlotCallback(state='residual', name='func_ressloss.png'),
        callbacks.PlotCallback(state='metric', name='func_metloss.png')
    )
    solver.fit(epochs)
