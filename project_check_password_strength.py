# Mamoun mohamed
# 21/11/2024
# password strength checker.

import re
import math
import secrets
import string
import unicodedata

class PasswordAnalyzer:
    def __init__(self):
        # Character set categories
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.punctuation = string.punctuation
        
        # Entropy calculation parameters
        self.entropy_base = 0
        self.entropy_bits = 0
    
    def analyze_password(self, password):
        """
        Comprehensive password strength analysis.
        
        Args:
            password (str): Password to analyze
        
        Returns:
            dict: Detailed password analysis results
        """
        # Normalize unicode characters
        normalized_password = unicodedata.normalize('NFKD', password)
        
        # Analyze character composition
        analysis = {
            'length': len(normalized_password),
            'lowercase_count': sum(1 for c in normalized_password if c in self.lowercase),
            'uppercase_count': sum(1 for c in normalized_password if c in self.uppercase),
            'digit_count': sum(1 for c in normalized_password if c in self.digits),
            'special_char_count': sum(1 for c in normalized_password if c in self.punctuation),
            'unicode_chars': len(set(normalized_password))
        }
        
        # Calculate character set size
        char_sets = set()
        if any(c in self.lowercase for c in normalized_password):
            char_sets.add(self.lowercase)
        if any(c in self.uppercase for c in normalized_password):
            char_sets.add(self.uppercase)
        if any(c in self.digits for c in normalized_password):
            char_sets.add(self.digits)
        if any(c in self.punctuation for c in normalized_password):
            char_sets.add(self.punctuation)
        
        # Entropy calculation
        unique_chars = len(set(normalized_password))
        total_possible_chars = sum(len(char_set) for char_set in char_sets)
        self.entropy_base = total_possible_chars
        self.entropy_bits = analysis['length'] * math.log2(total_possible_chars)
        
        # Pattern detection
        analysis['patterns'] = {
            'sequential': bool(re.search(r'(123|abc|qwerty)', normalized_password.lower())),
            'repeating_chars': bool(re.search(r'(.)\1{2,}', normalized_password)),
            'common_substitutions': bool(re.search(r'[@]|[1!]|[0o]', normalized_password))
        }
        
        # Strength rating
        analysis['entropy_bits'] = round(self.entropy_bits, 2)
        analysis['strength_rating'] = self._rate_password_strength(analysis)
        
        return analysis
    
    def _rate_password_strength(self, analysis):
        """
        Rate password strength based on multiple factors.
        
        Args:
            analysis (dict): Password analysis details
        
        Returns:
            str: Strength rating
        """
        score = 0
        
        # Length scoring
        if analysis['length'] >= 16:
            score += 3
        elif analysis['length'] >= 12:
            score += 2
        elif analysis['length'] >= 8:
            score += 1
        
        # Character diversity scoring
        if analysis['lowercase_count'] > 0:
            score += 1
        if analysis['uppercase_count'] > 0:
            score += 1
        if analysis['digit_count'] > 0:
            score += 1
        if analysis['special_char_count'] > 0:
            score += 1
        
        # Penalize for patterns and weak characteristics
        for pattern, exists in analysis['patterns'].items():
            if exists:
                score -= 1
        
        # Entropy-based rating
        if self.entropy_bits > 60:
            score += 2
        elif self.entropy_bits > 40:
            score += 1
        
        # Determine strength category
        if score <= 1:
            return "Very Weak"
        elif score <= 3:
            return "Weak"
        elif score <= 5:
            return "Moderate"
        elif score <= 7:
            return "Strong"
        else:
            return "Very Strong"
    
    def generate_strong_password(self, length=16):
        """
        Generate a cryptographically secure password.
        
        Args:
            length (int): Desired password length
        
        Returns:
            str: Generated strong password
        """
        # Combine character sets for maximum entropy
        all_chars = self.lowercase + self.uppercase + self.digits + self.punctuation
        
        # Use secrets module for cryptographically secure random selection
        password = ''.join(secrets.choice(all_chars) for _ in range(length))
        return password

def main():
    analyzer = PasswordAnalyzer()
    
    while True:
        print("\n--- Password Security Tool ---")
        print("1. Analyze Password")
        print("2. Generate Strong Password")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            # Secure password input
            password = input("Enter password to analyze: ")
            results = analyzer.analyze_password(password)
            
            # Detailed output
            print("\n--- Password Analysis ---")
            print(f"Length: {results['length']}")
            print(f"Lowercase Characters: {results['lowercase_count']}")
            print(f"Uppercase Characters: {results['uppercase_count']}")
            print(f"Digits: {results['digit_count']}")
            print(f"Special Characters: {results['special_char_count']}")
            print(f"Unique Characters: {results['unicode_chars']}")
            print(f"Entropy: {results['entropy_bits']} bits")
            print(f"Strength: {results['strength_rating']}")
            
            # Pattern warnings
            print("\nWarnings:")
            for pattern, exists in results['patterns'].items():
                if exists:
                    print(f"- Detected {pattern.replace('_', ' ')} pattern")
        
        elif choice == '2':
            # Password generation
            length = int(input("Enter desired password length (default 16): ") or 16)
            generated_password = analyzer.generate_strong_password(length)
            print(f"\nGenerated Password: {generated_password}")
            
            # Analyze generated password
            gen_results = analyzer.analyze_password(generated_password)
            print(f"Password Strength: {gen_results['strength_rating']}")
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
