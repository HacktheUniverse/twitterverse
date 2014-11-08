def RK4_step(x, dt, flow):    # replaces x(t) by x(t + dt)
    n = len(x)
    k1 = [ dt * k for k in flow(x) ]
    x_temp = [ x[i] + k1[i] / 2 for i in range(n) ]
    k2 = [ dt * k for k in flow(x_temp) ]
    x_temp = [ x[i] + k2[i] / 2 for i in range(n) ]
    k3 = [ dt * k for k in flow(x_temp) ]
    x_temp = [ x[i] + k3[i] for i in range(n) ]
    k4 = [ dt * k for k in flow(x_temp) ]
    for i in range(n):
        x[i] += (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6

def RK4_adaptive_step(x, dt, flow, accuracy=1e-6):  # from Numerical Recipes
    SAFETY = 0.9; PGROW = -0.2; PSHRINK = -0.25;
    ERRCON = 1.89E-4; TINY = 1.0E-30
    n = len(x)
    scale = flow(x)
    scale = [ abs(x[i]) + abs(scale[i] * dt) + TINY for i in range(n) ]
    while True:
        dt /= 2
        x_half = [ x[i] for i in range(n) ]
        RK4_step(x_half, dt, flow)
        RK4_step(x_half, dt, flow)
        dt *= 2
        x_full = [ x[i] for i in range(n) ]
        RK4_step(x_full, dt, flow)
        Delta = [ x_half[i] - x_full[i] for i in range(n) ]
        error = max( abs(Delta[i] / scale[i]) for i in range(n) ) / accuracy
        if error <= 1:
            break;
        dt_temp = SAFETY * dt * error**PSHRINK
        if dt >= 0:
            dt = max(dt_temp, 0.1 * dt)
        else:
            dt = min(dt_temp, 0.1 * dt)
        if abs(dt) == 0.0:
            raise OverflowError("step size underflow")
    if error > ERRCON:
        dt *= SAFETY * error**PGROW
    else:
        dt *= 5
    for i in range(n):
        x[i] = x_half[i] + Delta[i] / 15
    return dt