history = []  # to store calculation history

while True:
    try:
        num1 = float(input("Give 1st number: "))
        num2 = float(input("Give 2nd number: "))
    except ValueError:
        print("❌ Invalid input! Please enter numbers only.")
        continue

    print("\nAvailable operators: +, -, *, /, %, **, //")
    operator = input("Give operator: ")

    result = None

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            print("❌ Division by zero is not allowed")
    elif operator == "%":
        if num2 != 0:
            result = num1 % num2
        else:
            print("❌ Modulus by zero is not allowed")
    elif operator == "**":
        result = num1 ** num2
    elif operator == "//":
        if num2 != 0:
            result = num1 // num2
        else:
            print("❌ Floor division by zero is not allowed")
    else:
        print("❌ Not a valid operator")

    if result is not None:
        print(f"✅ Result: {num1} {operator} {num2} = {result}")
        history.append(f"{num1} {operator} {num2} = {result}")

    # Ask next action
    choice = input("\nDo you want to (yes = continue / history = view history / clear = clear history / no = exit): ").lower()
    if choice == "no":
        print("👋 Exiting calculator... Goodbye!")
        break
    elif choice == "history":
        if history:
            print("\n📜 Calculation History:")
            for h in history:
                print(h)
        else:
            print("⚠️ No calculations yet.")
    elif choice == "clear":
        history.clear()
        print("🗑️ History cleared!")
