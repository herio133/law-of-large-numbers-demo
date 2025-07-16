import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 🎩 Theme setup
plt.style.use('seaborn-v0_8-darkgrid')
np.random.seed(42)  # luck favors the well-prepared
# 🎲 Dice rolling oracle
def roll_dice(n):
    return np.random.randint(1, 7, size=n)
# 💫 Compute relative frequency of rolling a 6
def compute_frequencies(outcomes):
    is_six = (outcomes == 6)
    return np.cumsum(is_six) / np.arange(1, len(outcomes) + 1)
# ✨ Animation spell
def animate_frequency(n_trials=1000):
    outcomes = roll_dice(n_trials)
    frequencies = compute_frequencies(outcomes)
    theoretical = 1 / 6

    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot([], [], lw=2, color='gold', label='Relative Frequency')
    ax.axhline(theoretical, color='crimson', linestyle='--', label='Theoretical (1/6)')
    ax.set_xlim(0, n_trials)
    ax.set_ylim(0, 1)
    ax.set_xlabel('Number of Trials')
    ax.set_ylabel('Relative Frequency of Rolling a 6 🎯')
    ax.set_title('🎲 Law of Large Numbers in Action: Rolling a Die Elegantly')
    ax.legend(loc='upper right')

    def update(frame):
        x = np.arange(1, frame + 1)
        y = frequencies[:frame]
        line.set_data(x, y)
        return line,

    ani = animation.FuncAnimation(
        fig, update, frames=n_trials, interval=10, blit=True, repeat=False
    )

    plt.show()

# 🌟 Cast the spell
animate_frequency(n_trials=1000)
