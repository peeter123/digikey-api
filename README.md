KiCost plug-in for Digi-Key API
=================================
This is an experimental plug-in to allow KiCost to do native Digi-Key API requests.

The plug-in is based on the [Python Client for Digikey API](https://github.com/peeter123/digikey-api)
by [Peter Oostewechel](https://github.com/peeter123).

I'm not using the original project as a module because it pulls some rare dependencies.

The license is GPL v3 as the original work.

# Quickstart

- Register at Digi-Key. You need a valid user in order to register an application and in order to authenticate.
- Go to the API portal: [Digi-Key API Solutions](https://developer.digikey.com/get_started)
- Login to Digi-Key from the API portal
- Create an [organization](https://developer.digikey.com/teams)
- Choose the `Production Apps` operation
- Create a production app
  - Choose a `Production App name`
  - Use `https://localhost:8139/digikey_callback` for the OAuth Callback. So you can authorize the use of the app.
  - Give a description
  - Enable the `Product Information` API
  - Click `Add production app`
- Now select your newly created `Production App`
- In the `Credential` section enable the options to show the `Client ID` and `Client Secret`
- Copy these values to a file named `config.txt` containing:

```
DIGIKEY_CLIENT_ID = Client_ID_Value_for_your_app
DIGIKEY_CLIENT_SECRET = Client_Secret_Value_for_your_app
```

- Create a folder `~/.config/kicost_digikey_api_v3`
- Store the config.txt file
- Now install the plug-in:
  - Clone the git repo somewhere using `git clone https://github.com/set-soft/kicost-digikey-api-v3.git`
  - Enter to `kicost-digikey-api-v3`
  - Install it using `pip3 install -e .`
- Now test the plug-in:
  - run `python3 test_production.py`
  - A browser window will pop-up asking to login to Digi-Key. Login.
  - Choose the allow option to enable the token.
  - Now you'll load a local page, allow it.
  - Now the token is stored on disk and you won't need to confirm it for months.
  - You should get the information for Digi-Key part 296-6501-6-ND

