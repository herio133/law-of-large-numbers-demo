import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import random

class BellTestSimulator:
    """
    Demonstrates Bell's Inequality and its quantum violation
    
    The CHSH inequality: S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')| ≤ 2
    Where E(x,y) is the correlation between measurements at angles x and y
    
    Classical physics: S ≤ 2
    Quantum mechanics: S ≤ 2√2 ≈ 2.83
    """
    
    def __init__(self):
        self.sqrt2 = np.sqrt(2)
        
    def classical_correlation(self, angle_a, angle_b, num_trials=10000):
        """
        Simulate classical correlation using hidden variables
        Each particle has predetermined results for all possible measurements
        """
        correlations = []
        
        for _ in range(num_trials):
            # Generate hidden variables (predetermined results for all angles)
            # Each particle has a random orientation λ
            lambda_hidden = random.uniform(0, 2*np.pi)
            
            # Classical prediction: result depends on angle relative to hidden variable
            result_a = 1 if np.cos(angle_a - lambda_hidden) > 0 else -1
            result_b = 1 if np.cos(angle_b - lambda_hidden) > 0 else -1
            
            correlations.append(result_a * result_b)
            
        return np.mean(correlations)
    
    def quantum_correlation(self, angle_a, angle_b):
        """
        Quantum mechanical prediction for entangled pairs
        E(a,b) = -cos(a - b) for singlet state
        """
        return -np.cos(angle_a - angle_b)
    
    def simulate_bell_test(self, num_trials=10000):
        """
        Perform the complete Bell test with optimal angles
        
        Optimal angles for maximum quantum violation:
        a = 0°, a' = 45°, b = 22.5°, b' = 67.5°
        """
        # Convert to radians
        a = 0
        a_prime = np.pi/4          # 45°
        b = np.pi/8               # 22.5°
        b_prime = 3*np.pi/8       # 67.5°
        
        print("🔬 Bell's Inequality Test")
        print("=" * 50)
        print(f"Measurement angles:")
        print(f"  a = {np.degrees(a):.1f}°,  a' = {np.degrees(a_prime):.1f}°")
        print(f"  b = {np.degrees(b):.1f}°,  b' = {np.degrees(b_prime):.1f}°")
        print()
        
        # Classical predictions (using hidden variable model)
        print("📊 Classical Physics Predictions (Hidden Variables):")
        E_ab_classical = self.classical_correlation(a, b, num_trials)
        E_ab_prime_classical = self.classical_correlation(a, b_prime, num_trials)
        E_a_prime_b_classical = self.classical_correlation(a_prime, b, num_trials)
        E_a_prime_b_prime_classical = self.classical_correlation(a_prime, b_prime, num_trials)
        
        S_classical = abs(E_ab_classical - E_ab_prime_classical + 
                         E_a_prime_b_classical + E_a_prime_b_prime_classical)
        
        print(f"  E(a,b)   = {E_ab_classical:.4f}")
        print(f"  E(a,b')  = {E_ab_prime_classical:.4f}")
        print(f"  E(a',b)  = {E_a_prime_b_classical:.4f}")
        print(f"  E(a',b') = {E_a_prime_b_prime_classical:.4f}")
        print(f"  S_classical = {S_classical:.4f}")
        print(f"  Classical limit: S ≤ 2.000")
        print(f"  Status: {'✓ Satisfied' if S_classical <= 2.0 else '✗ VIOLATED!'}")
        print()
        
        # Quantum predictions
        print("🌟 Quantum Mechanics Predictions:")
        E_ab_quantum = self.quantum_correlation(a, b)
        E_ab_prime_quantum = self.quantum_correlation(a, b_prime)
        E_a_prime_b_quantum = self.quantum_correlation(a_prime, b)
        E_a_prime_b_prime_quantum = self.quantum_correlation(a_prime, b_prime)
        
        S_quantum = abs(E_ab_quantum - E_ab_prime_quantum + 
                       E_a_prime_b_quantum + E_a_prime_b_prime_quantum)
        
        print(f"  E(a,b)   = {E_ab_quantum:.4f}")
        print(f"  E(a,b')  = {E_ab_prime_quantum:.4f}")
        print(f"  E(a',b)  = {E_a_prime_b_quantum:.4f}")
        print(f"  E(a',b') = {E_a_prime_b_prime_quantum:.4f}")
        print(f"  S_quantum = {S_quantum:.4f}")
        print(f"  Quantum limit: S ≤ {2*self.sqrt2:.3f}")
        print(f"  Classical limit: S ≤ 2.000")
        print(f"  Status: {'🚨 VIOLATES CLASSICAL PHYSICS!' if S_quantum > 2.0 else '✓ Within classical bounds'}")
        
        return {
            'classical': {
                'correlations': [E_ab_classical, E_ab_prime_classical, 
                               E_a_prime_b_classical, E_a_prime_b_prime_classical],
                'S': S_classical
            },
            'quantum': {
                'correlations': [E_ab_quantum, E_ab_prime_quantum,
                               E_a_prime_b_quantum, E_a_prime_b_prime_quantum],
                'S': S_quantum
            },
            'angles': [a, a_prime, b, b_prime]
        }
    
    def plot_correlation_comparison(self, num_points=100):
        """
        Plot classical vs quantum correlations for different angle differences
        """
        angle_diffs = np.linspace(0, np.pi, num_points)
        classical_corrs = []
        quantum_corrs = []
        
        for diff in angle_diffs:
            # For classical, use average over many hidden variable realizations
            classical_corrs.append(self.classical_correlation(0, diff, 1000))
            quantum_corrs.append(self.quantum_correlation(0, diff))
        
        plt.figure(figsize=(12, 8))
        
        # Main correlation plot
        plt.subplot(2, 2, 1)
        plt.plot(np.degrees(angle_diffs), classical_corrs, 'b-', 
                linewidth=2, label='Classical (Hidden Variables)', alpha=0.8)
        plt.plot(np.degrees(angle_diffs), quantum_corrs, 'r-', 
                linewidth=2, label='Quantum Mechanics')
        plt.xlabel('Angle Difference (degrees)')
        plt.ylabel('Correlation E(θ)')
        plt.title('Classical vs Quantum Correlations')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Bell inequality violation plot
        plt.subplot(2, 2, 2)
        angles_for_bell = np.linspace(0, np.pi/2, 50)
        S_values_classical = []
        S_values_quantum = []
        
        for base_angle in angles_for_bell:
            # Use angles optimized for Bell violation
            a, a_prime = 0, base_angle
            b, b_prime = base_angle/2, 3*base_angle/2
            
            # Classical S
            E1 = self.classical_correlation(a, b, 500)
            E2 = self.classical_correlation(a, b_prime, 500)
            E3 = self.classical_correlation(a_prime, b, 500)
            E4 = self.classical_correlation(a_prime, b_prime, 500)
            S_classical = abs(E1 - E2 + E3 + E4)
            S_values_classical.append(S_classical)
            
            # Quantum S
            E1_q = self.quantum_correlation(a, b)
            E2_q = self.quantum_correlation(a, b_prime)
            E3_q = self.quantum_correlation(a_prime, b)
            E4_q = self.quantum_correlation(a_prime, b_prime)
            S_quantum = abs(E1_q - E2_q + E3_q + E4_q)
            S_values_quantum.append(S_quantum)
        
        plt.plot(np.degrees(angles_for_bell), S_values_classical, 'b-', 
                linewidth=2, label='Classical', alpha=0.8)
        plt.plot(np.degrees(angles_for_bell), S_values_quantum, 'r-', 
                linewidth=2, label='Quantum')
        plt.axhline(y=2, color='black', linestyle='--', alpha=0.7, 
                   label='Classical Limit (S = 2)')
        plt.axhline(y=2*self.sqrt2, color='red', linestyle=':', alpha=0.7,
                   label=f'Quantum Limit (S = 2√2)')
        plt.xlabel('Base Angle (degrees)')
        plt.ylabel('Bell Parameter S')
        plt.title('Bell Inequality: S vs Measurement Angles')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Violation magnitude
        plt.subplot(2, 2, 3)
        violation = np.array(S_values_quantum) - 2
        plt.plot(np.degrees(angles_for_bell), violation, 'purple', linewidth=2)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        plt.fill_between(np.degrees(angles_for_bell), 0, violation, 
                        where=(violation > 0), alpha=0.3, color='red',
                        label='Quantum Violation Region')
        plt.xlabel('Base Angle (degrees)')
        plt.ylabel('Violation Amount (S - 2)')
        plt.title('Magnitude of Bell Inequality Violation')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Historical context
        plt.subplot(2, 2, 4)
        plt.text(0.1, 0.8, "🏆 Nobel Prize 2022", fontsize=16, fontweight='bold',
                transform=plt.gca().transAxes)
        plt.text(0.1, 0.7, "Alain Aspect, John Clauser,\nAnton Zeilinger", 
                transform=plt.gca().transAxes, fontsize=12)
        plt.text(0.1, 0.5, "Key Insights:", fontweight='bold', 
                transform=plt.gca().transAxes)
        plt.text(0.1, 0.4, "• Local realism is false", 
                transform=plt.gca().transAxes)
        plt.text(0.1, 0.3, "• Nature is fundamentally\n  non-local", 
                transform=plt.gca().transAxes)
        plt.text(0.1, 0.2, "• Einstein was wrong about\n  'spooky action'", 
                transform=plt.gca().transAxes)
        plt.text(0.1, 0.05, "• Enables quantum tech:\n  computing, cryptography", 
                transform=plt.gca().transAxes)
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()

# Demonstration
def main():
    print("🌟 Bell's Inequality: The Ultimate Test of Reality")
    print("=" * 60)
    print("This demonstrates why Einstein said quantum mechanics")
    print("exhibits 'spooky action at a distance' - and why he was right!")
    print()
    
    bell_test = BellTestSimulator()
    
    # Run the Bell test
    results = bell_test.simulate_bell_test(num_trials=50000)
    
    print("\n" + "="*60)
    print("🎯 CONCLUSION:")
    print("="*60)
    
    if results['quantum']['S'] > 2.0:
        print("🚨 QUANTUM MECHANICS VIOLATES BELL'S INEQUALITY!")
        print(f"   Quantum S = {results['quantum']['S']:.4f} > 2.000")
        print("   This proves:")
        print("   • No hidden variables can explain quantum mechanics")
        print("   • Reality is fundamentally non-local")
        print("   • Einstein's 'local realism' is incorrect")
        print("   • The universe is genuinely quantum mechanical!")
    
    print(f"\n📊 Violation strength: {((results['quantum']['S'] - 2) / (2*np.sqrt(2) - 2) * 100):.1f}% of maximum possible")
    
    # Create visualizations
    print("\n📈 Generating comparison plots...")
    bell_test.plot_correlation_comparison()
    
    print("\n💡 Physical Interpretation:")
    print("   • Classical: Particles have predetermined properties")
    print("   • Quantum: Properties don't exist until measured")
    print("   • The correlations are stronger in quantum case!")
    print("   • This enables quantum computing and cryptography")

if __name__ == "__main__":
    main()
