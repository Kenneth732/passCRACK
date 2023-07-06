const { execSync } = require('child_process');

// Run the nmcli command to get the Wi-Fi profiles
const profilesCommand = 'nmcli connection show | grep -i wifi | awk \'{print $1}\'';
const profilesOutput = execSync(profilesCommand).toString().trim();
const profiles = profilesOutput.split('\n');

// Iterate over the profiles and retrieve the passwords
for (const profile of profiles) {
  try {
    const passwordCommand = `nmcli connection show "${profile}" | grep -i 802-11-wireless-security.psk | awk '{print $2}'`;
    const passwordOutput = execSync(passwordCommand).toString().trim();
    
    console.log(`Wi-Fi Profile: ${profile}, Password: ${passwordOutput}`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    console.log(`Wi-Fi Profile: ${profile}, Password: Not available`);
  }
}



