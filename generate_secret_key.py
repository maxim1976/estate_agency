"""
Generate a secure SECRET_KEY for Django production deployment
Run this locally and add the output to Railway environment variables
"""

from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("\n" + "="*70)
    print("🔐 DJANGO SECRET KEY GENERATOR")
    print("="*70)
    print("\nGenerated SECRET_KEY:")
    print("-"*70)
    print(secret_key)
    print("-"*70)
    print("\n📋 Copy this key and add it to Railway Dashboard:")
    print("   1. Go to Railway Dashboard → Your Service → Variables")
    print("   2. Add new variable:")
    print("      Name:  SECRET_KEY")
    print(f"      Value: {secret_key}")
    print("\n⚠️  NEVER commit this key to Git!")
    print("="*70 + "\n")
