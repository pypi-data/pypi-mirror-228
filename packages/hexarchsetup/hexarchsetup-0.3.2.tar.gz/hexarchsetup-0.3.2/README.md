# HexArchSetup
_This project automatically generates a project structure following the Hexagonal Architecture in Python. It is highly customizable to include user-defined modules._

## 🛠️ Installation

### Option 1: Using pip

```bash
pip install hexarchsetup
```

Then run:

```bash
hexsetup
```

### Option 2: Direct Execution

```bash
git clone https://github.com/username/HexArchSetup.git
cd HexArchSetup
python -m src.main
```

## 🚀 Usage

After installation, you will be prompted to input the project name and the names of the modules you wish to generate.

## 📦 Generated Directory Structure

```plaintext
.
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── src
│   ├── adapters
│   │   ├── api_adapter.py
│   │   └── db_adapter.py
│   ├── config
│   │   └── settings.py
│   ├── core
│   │   ├── application_services
│   │   │   ├── module1_services.py
│   │   │   └── module2_services.py
│   │   └── domain
│   │       ├── interfaces
│   │       │   ├── module1_interface.py
│   │       │   └── module2_interface.py
│   │       └── models
│   │           ├── module1.py
│   │           └── module2.py
│   ├── database
│   │   └── models.py
│   ├── dependencies
│   │   └── auth.py
│   ├── main.py
│   └── modules
│       ├── module1
│       │   ├── api
│       │   │   ├── routes.py
│       │   │   └── schemas.py
│       │   └── services.py
│       └── module2
│           ├── api
│           │   ├── routes.py
│           │   └── schemas.py
│           └── services.py
├── templates
│   └── index.html
└── tests
    ├── adapters
    │   ├── test_api_adapter.py
    │   └── test_db_adapter.py
    ├── config
    │   └── test_settings.py
    ├── core
    │   ├── application_services
    │   │   ├── test_module1_services.py
    │   │   └── test_module2_services.py
    │   └── domain
    │       ├── interfaces
    │       │   ├── test_module1_interface.py
    │       │   └── test_module2_interface.py
    │       └── models
    │           ├── test_module1.py
    │           └── test_module2.py
    ├── database
    │   └── test_models.py
    ├── dependencies
    │   └── test_auth.py
    ├── test_main.py
    └── modules
        ├── module1
        │   ├── api
        │   │   ├── test_routes.py
        │   │   └── test_schemas.py
        │   └── test_services.py
        └── module2
            ├── api
            │   ├── test_routes.py
            │   └── test_schemas.py
            └── test_services.py
```

## 📚 Technologies Used

- Python 3.11.4
- JSON for structure templates

## 📋 License

This project is under the MIT License. See the `LICENSE` file for more details.
