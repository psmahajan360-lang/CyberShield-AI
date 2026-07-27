print("===================================")
print("      CyberShield AI v1.0")
print(" AI Phishing Detection Platform")
print("===================================")

url = input("Enter Website URL: ").strip()

if url == "":

    print(" Please enter a website URL.")
else:
       
 if url.startswith("https://"):
        print("✅ Valid URL format.")
        print("Analyzing:", url)
 else:
        print("❌ Invalid URL. Please start with https://")


    