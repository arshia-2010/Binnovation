from supabase import create_client, Client

# Supabase Credentials
SUPABASE_URL = "https://tebznbxgqyexhjkdyllv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlYnpuYnhncXlleGhqa2R5bGx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg2NjIzNTEsImV4cCI6MjA1NDIzODM1MX0.FjahnOhloOFtCumUSBnafRXoy-nUmh1Aph_f-nAqtSc"

# Connect to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch all rows from a table
def get_all_data():
    response = supabase.from_("metals_data").select("*").execute()
    return response.data if response.data else response.error

# Insert a new row into the table
def insert_data(material, reflectivity, wavelength):
    response = supabase.from_("metals_data").insert([
        {"material": material, "reflectivity": reflectivity, "wavelength": wavelength}
    ]).execute()
    return response.data if response.data else response.error
    
# to check if the connectivity is established or not
try:
    # Try to create a connection
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Attempt a simple query to check connectivity
    response = supabase.from_("materials").select("reflectivity_average").limit(1).execute()
    
    if response.data:
        print("Supabase Connection Successful!")
    else:
        print("Connected, but no data found in the table.")

except Exception as e:
    print("Error connecting to Supabase:", e)