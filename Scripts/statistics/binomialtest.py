from scipy.stats import binomtest

def run_test(name, k, n):
    res = binomtest(k, n, p=0.0, alternative="greater")
    print(f"{name}")
    print(f"  Beobachtete Wechsel: {k}/{n} ({k/n:.2%})")
    print(f"  p-Wert (Binomialtest gegen p=0): {res.pvalue:.3e}")
    print("-" * 60)

def main():

    # Persona Sycophancy
    n_persona = 470

    run_test(
        "Persona Sycophancy – DeepSeek-Chat",
        k=161,
        n=n_persona
    )

    run_test(
        "Persona Sycophancy – DeepSeek-Reasoner",
        k=160,
        n=n_persona
    )


    # Preference Sycophancy
    n_preference = 1265

    run_test(
        "Preference Sycophancy – DeepSeek-Chat",
        k=725,
        n=n_preference
    )

    run_test(
        "Preference Sycophancy – DeepSeek-Reasoner",
        k=627,
        n=n_preference
    )

if __name__ == "__main__":
    main()
