import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def digital_filter(input_signal, b, a):
    output_signal = signal.lfilter(b, a, input_signal)
    return output_signal


def dirac():
    n_samples = 1000
    t = np.linspace(0, 1, n_samples)
    input_signal = np.zeros(n_samples)
    input_signal[0] = 1
    return input_signal


def create_random_filter(num_poles, num_zeros):
    #can not devide by zerro
    if num_poles == 0:
        num_poles = 1
    if num_zeros == 0:
        num_zeros = 1

    # Generate random pole and zero locations within a range of 1
    poles = np.random.uniform(-1, 1, size=num_poles)
    zeros = np.random.uniform(-1, 1, size=num_zeros)

    # Construct the polynomials
    a = np.poly(poles)
    b = np.poly(zeros)

    b /= np.sum(np.abs(b))
    a /= np.sum(np.abs(a))

    b = np.round(b, decimals=1)
    a = np.round(a, decimals=1)

    
    zpk = signal.zpk2tf(zeros, poles, 1)
    z = signal.TransferFunction(zpk[0], zpk[1], dt=1.0)

    return b, a


# Get user input for the number of poles and zeros
num_poles = int(input("Enter the number of poles: "))
num_zeros = int(input("Enter the number of zeros: "))

# Filter creation
b, a = create_random_filter(num_poles, num_zeros)
input_signal = dirac()
output_signal = digital_filter(input_signal, b, a)

# Calculate pole and zero locations
poles = np.roots(a)
zeros = np.roots(b)

# Transfer function
numerator = ' + '.join([f"{b[i]} * z^(-{i})" for i in range(len(b))])
denominator = ' + '.join([f"{a[i]} * z^(-{i})" for i in range(1, len(a))])
transfer_function = f"H(z) = ({numerator}) / ({denominator})"
print("\nTransfer Function:")
print(transfer_function)

# Output first ten values
filter_formula = "y[n] = " + " + ".join(f"{b[i]} * x[n-{i}]" for i in range(len(b)))
filter_formula += " - " + " - ".join(f"{a[i]} * y[n-{i}]" for i in range(1, len(a)))
print("Filter Formula:", filter_formula)
print("Output Signal:")
for i in range(5):
    print(f"y[{i}] = {output_signal[i]}")
print("Input Signal:")
for i in range(5):
    print(f"x[{i}] = {input_signal[i]}")
    
# Display poles and zeros
print("Pole positions:")
for pole in poles:
    print(f"({np.real(pole):.1f}, {np.imag(pole):.1f})")

print("\nZero positions:")
for zero in zeros:
    print(f"({np.real(zero):.1f}, {np.imag(zero):.1f})")

# Stability
is_stable = np.all(np.abs(poles) < 1)
print("\nSystem Stability: ", "Stable" if is_stable else "Unstable")

# Argand diagram
plt.figure(figsize=(8, 8))
circle = plt.Circle((0, 0), 1, color='gray', fill=False, linestyle='dashed')
ax = plt.gca()
ax.add_patch(circle)
plt.scatter(np.real(poles), np.imag(poles), color='red', marker='x', label='Poles')
plt.scatter(np.real(zeros), np.imag(zeros), color='green', marker='o', label='Zeros')
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title('Argand Diagram')
plt.grid(True)
plt.legend()
plt.show()
