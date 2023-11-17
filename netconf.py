from ncclient import manager
import requests

# Define device details
device = {
    'host': '172.17.0.1',
    'port': 830,
    'username': 'hilbelinka5142',
    'password': 'M!styhair48',
    'hostkey_verify': False,
    'device_params': {'name': 'csr'}
}

# Connect to the device
with manager.connect(**device) as m:
    # Your NETCONF operations will go here
    pass

# NETCONF RPC to get the running configuration
get_running_config_template = """
<filter>
  <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
    <schemas/>
    <datastores>
      <datastore>
        <name>running</name>
      </datastore>
    </datastores>
  </netconf-state>
</filter>
"""

try:
    # Connect to the device
    with manager.connect(**device) as m:
        # Send NETCONF request to get the running configuration
        response = m.get(('subtree', get_running_config_template))

        # Print the XML response
        print(response.xml)

except Exception as e:
    print(f"Error: {e}")


# NETCONF RPC to edit the configuration (make three changes)
edit_config_template = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>new_hostname</hostname>  <!-- Change 1: Set a new hostname -->
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <description>Updated interface description</description>  <!-- Change 2: Update interface description -->
        <ip>
          <address>
            <primary>
              <address>192.168.1.1</address>  <!-- Change 3: Update IP address -->
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </GigabitEthernet>
    </interface>
  </native>
</config>
"""

try:
    # Connect to the device
    with manager.connect(**device) as m:
        # Send NETCONF request to edit the configuration
        response = m.edit_config(target='running', config=('replace', edit_config_template))

        # Print the XML response
        print(response.xml)

except Exception as e:
    print(f"Error: {e}")


# NETCONF RPC to verify the changes
verify_template = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>  <!-- Verify Change 1: Hostname -->
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <description/>  <!-- Verify Change 2: Interface Description -->
        <ip>
          <address>
            <primary>
              <address/>  <!-- Verify Change 3: IP Address -->
            </primary>
          </address>
        </ip>
      </GigabitEthernet>
    </interface>
  </native>
</filter>
"""

try:
    # Connect to the device
    with manager.connect(**device) as m:
        # Send NETCONF request to verify the changes
        response = m.get_config(source='running', filter=('subtree', verify_template))

        # Print the XML response
        print(response.xml)

except Exception as e:
    print(f"Error: {e}")



# Webex Teams API details
webex_teams_token = 'MzU3YjZmYzktZjc4Zi00ZmYxLTk1MjAtMzNjZDk0NWEzZmRkNzY5NDU4YjktYzRk_P0A1_36820416-bfff-433a-84bf-39585b2b3f67'
webex_teams_room_id = '65579F6D-D940-01BB-0119-44BE86C70119'

# Message to announce the update
message = "Network configuration changes have been successfully verified."

# Webex Teams API request
url = f"https://api.ciscospark.com/v1/messages"
headers = {
    'Authorization': f'Bearer {webex_teams_token}',
    'Content-Type': 'application/json'
}
payload = {
    'roomId': webex_teams_room_id,
    'text': message
}

try:
    # Send the Webex Teams API request
    response = requests.post(url, headers=headers, json=payload)

    # Print the response from Webex Teams
    print(response.json())

except Exception as e:
    print(f"Error: {e}")
