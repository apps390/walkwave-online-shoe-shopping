import razorpay

def test_razorpay_client():
    try:
        client = razorpay.Client(auth=("your_key_id", "your_key_secret"))
        print("Razorpay client created successfully")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_razorpay_client()