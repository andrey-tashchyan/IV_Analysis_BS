from data_loader import download_data
from vol_analysis import analyze_volatility
from update_spot import update_spot_price


print("=== Début main ===")


# Ask the user for a ticker
ticker = input("Enter a stock ticker (e.g., AAPL, ^TSLA): ").strip().upper()
if ticker == "":
    print("❌ No ticker provided. Exiting.")
    exit()

# Step 1 : Download data
print("Calling download_data()...")
success = download_data(ticker)
if not success:
    print("❌ Download failed. Exiting.")
    exit()
print("Download_data() finished")

# Step 2 : Updating data
print("Appel de update_spot_price()...")
update_spot_price(ticker)
print("Update_spot_price() terminé")

# Step 3 : Analyze and draw the curve
print("Calling analyze_volatility()...")
analyze_volatility(ticker)
print("analyze_volatility() finished")

print("=== End of main ===")