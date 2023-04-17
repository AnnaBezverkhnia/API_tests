from typing import Any

templates: dict[str, Any] = {
    '''
    The dictionary holds user templates for all @N devices models.
    Its items are used in the test, when we want to check if
    a correct template is returned when requesting api/dir/template endpoint.

    For example, the assertation could look:

    rsp = dir.get_template()
    assert rsp['users'] == templates['vario']
    '''

  # ----------------------------------------------------------------------------
  #  VARIO - SAFETY - FORCE
  # ----------------------------------------------------------------------------
  'vario': [
    {
      "uuid": "",
      "deleted": False,
      "owner": "",
      "name": "",
      "photo": "",
      "email": "",
      "treepath": "/",
      "virtNumber": "",
      "deputy": "",
      "buttons": "",
      "callPos": [
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          }
        ],
      "access": {
          "validFrom": "0",
          "validTo": "0",
          "accessPoints": [
            {
              "enabled": True,
              "profiles": ""
            },
            {
              "enabled": True,
              "profiles": ""
            }
          ],
          "virtCard": "",
          "card": [
            "", ""
          ],
          "pin": "",
          "accessException": False,
          "code": [
            "", "", "", ""
          ],
          "licensePlates": "",
          "liftFloors": ""
        },
      "timestamp": 0
    }
  ],
  # ----------------------------------------------------------------------------
  #  STYLE
  # ----------------------------------------------------------------------------
  'style': [
    {
      "uuid": "",
      "deleted": False,
      "owner": "",
      "recordType": 0,
      "name": "",
      "photo": "",
      "highlighting": False,
      "email": "",
      "treepath": "/",
      "virtNumber": "",
      "deputy": "",
      "callPos": [
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          }
        ],
      "access": {
          "validFrom": "0",
          "validTo": "0",
          "accessPoints": [
            {
              "enabled": True,
              "profiles": ""
            },
            {
              "enabled": True,
              "profiles": ""
            }
          ],
          "pairingExpired": False,
          "virtCard": "",
          "card": [
            "", ""
          ],
          "mobkey": "",
          "fpt": "",
          "pin": "",
          "accessException": False,
          "code": [
            "", "", "", ""
          ],
          "licensePlates": "",
          "liftFloors": ""
        },
      "timestamp": 0
    }
  ],
  # ----------------------------------------------------------------------------
  #  BASE
  # ----------------------------------------------------------------------------
  'base': [
    {
      "uuid": "",
      "deleted": False,
      "owner": "",
      "name": "",
      "email": "",
      "deputy": "",
      "buttons": "",
      "callPos": [
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          }
        ],
      "access": {
          "validFrom": "0",
          "validTo": "0",
          "accessPoints": [
            {
              "enabled": True,
              "profiles": ""
            },
            {
              "enabled": True,
              "profiles": ""
            }
          ],
          "card": [
            "", ""
          ],
          "pin": "",
          "accessException": False,
          "code": [
            "", ""
          ],
          "licensePlates": ""
        },
      "timestamp": 0
    }
  ],

  # ----------------------------------------------------------------------------
  #  UNI
  # ----------------------------------------------------------------------------
  'uni': [
    {
      "uuid": "",
      "deleted": False,
      "owner": "",
      "name": "",
      "buttons": "",
      "callPos": [
          {
              "peer": "",
              "profiles": "",
              "grouped": False
          },
          {
              "peer": "",
              "profiles": "",
              "grouped": False
          },
          {
              "peer": "",
              "profiles": "",
              "grouped": False
          }
            ],
      "access": {
          "code": [
              ""
          ]
          },
      "timestamp": 0
    }
  ],

  # ----------------------------------------------------------------------------
  #  SOLO - VERSO = VERSO 2.0
  # ----------------------------------------------------------------------------
  'verso': [
    {
      "uuid": "",
      "deleted": False,
      "owner": "",
      "name": "",
      "photo": "",
      "email": "",
      "treepath": "/",
      "virtNumber": "",
      "deputy": "",
      "buttons": "",
      "callPos": [
          {
              "peer": "",
              "profiles": "",
              "grouped": False,
              "ipEye": ""
          },
          {
              "peer": "",
              "profiles": "",
              "grouped": False,
              "ipEye": ""
          },
          {
              "peer": "",
              "profiles": "",
              "grouped": False,
              "ipEye": ""
          }
          ],
      "access": {
            "validFrom": "0",
            "validTo": "0",
            "accessPoints": [
                {
                  "enabled": True,
                  "profiles": ""
                },
                {
                  "enabled": True,
                  "profiles": ""
                }
            ],
            "pairingExpired": False,
            "virtCard": "",
            "card": [
                "", ""
            ],
            "mobkey": "",
            "fpt": "",
            "pin": "",
            "accessException": False,
            "code": [
                "", "", "", ""
            ],
            "licensePlates": "",
            "liftFloors": ""
            },
      "timestamp": 0
    }
  ],
  # ----------------------------------------------------------------------------
  #  AU - AU2 - AUM
  # ----------------------------------------------------------------------------
  'accessunit': [
    {
      "uuid": "",
      "deleted": False,
      "owner": "",
      "name": "",
      "email": "",
      "access": {
          "validFrom": "0",
          "validTo": "0",
          "accessPoints": [
            {
              "enabled": True,
              "profiles": ""
            },
            {
              "enabled": True,
              "profiles": ""
            }
          ],
          "pairingExpired": False,
          "virtCard": "",
          "card": [
            "", ""
          ],
          "mobkey": "",
          "fpt": "",
          "pin": "",
          "accessException": False,
          "code": [
            "", ""
          ],
          "licensePlates": "",
          "liftFloors": ""
        },
      "timestamp": 0
      }
    ],

  # ----------------------------------------------------------------------------
  #  IPONE
  # ----------------------------------------------------------------------------
  'ipone': [
    {
      "uuid": "",
      "deleted": False,
      "owner": "",
      "name": "",
      "photo": "",
      "email": "",
      "deputy": "",
      "buttons": "",
      "callPos": [
          {
            "peer": "",
            "profiles": "",
            "grouped": False
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False
          }
        ],
      "access": {
          "validFrom": "0",
          "validTo": "0",
          "accessPoints": [
            {
              "enabled": True,
              "profiles": ""
            },
            {
              "enabled": True,
              "profiles": ""
            }
          ],
          "pin": "",
          "accessException": False,
          "code": [
            "", "", "", ""
          ],
          "licensePlates": ""
        },
      "timestamp": 0
    }
  ],
  # ----------------------------------------------------------------------------
  #  VIDEOKIT
  # ----------------------------------------------------------------------------
  'videokit':  [
      {
        "uuid": "",
        "deleted": False,
        "owner": "",
        "name": "",
        "email": "",
        "virtNumber": "",
        "deputy": "",
        "buttons": "",
        "callPos": [
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False,
            "ipEye": ""
          }
        ],
        "access": {
          "validFrom": "0",
          "validTo": "0",
          "accessPoints": [
            {
              "enabled": True,
              "profiles": ""
            },
            {
              "enabled": True,
              "profiles": ""
            }
          ],
          "pin": "",
          "accessException": False,
          "code": [
            "", "", "", ""
          ],
          "licensePlates": ""
        },
        "timestamp": 0
      }
  ],
  # ----------------------------------------------------------------------------
  #  AUDIOKIT
  # ----------------------------------------------------------------------------
  'audiokit': [
      {
        "uuid": "",
        "deleted": False,
        "owner": "",
        "name": "",
        "email": "",
        "virtNumber": "",
        "deputy": "",
        "buttons": "",
        "callPos": [
          {
            "peer": "",
            "profiles": "",
            "grouped": False
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False
          },
          {
            "peer": "",
            "profiles": "",
            "grouped": False
          }
        ],
        "access": {
          "validFrom": "0",
          "validTo": "0",
          "accessPoints": [
            {
              "enabled": True,
              "profiles": ""
            },
            {
              "enabled": True,
              "profiles": ""
            }
          ],
          "pin": "",
          "accessException": False,
          "code": [
            "", "", "", ""
          ],
          "licensePlates": ""
        },
        "timestamp": 0
      }
    ]
}
