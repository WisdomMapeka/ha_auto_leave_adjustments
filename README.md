### Ha Auto Leave Adjustments

This is an application that automate the leave allocation accumulations of employess. Instead of accumulating monthlys leaves manually, this automates the process.

# How This work
Set the leave types and the number of leave days to be used for leave allocation accumulations in this doctype `Ha Leave Adjustments Settings`

Now When you create payroll entry, when you click submit button, which sometimes is found on the list view under actions button, the set number of leaves is automatically added to the new leaves which will update other fields that uses leave allocation number.

This only applies to allocations that are not canceled also that are not drafts but submited.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app ha_auto_leave_adjustments
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/ha_auto_leave_adjustments
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
