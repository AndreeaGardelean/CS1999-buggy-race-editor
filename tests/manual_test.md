## Test Report - 9th June 2021

### Modules tested:
* 'Create buggy' form page
* Buggy cost
* Json details

### Test cases:
* Form autofill
* Modal pop-up
* Error messages
* Buggy total cost
* Buggy Json format

#### Test case 1: Form autofill
If the 'Autofill' button is pressed the form inputs are randomly filled with the according data. This gives the expected outputs.
If the user completes the form and the 'Autofill' button is pressed the form will not keep the user data and change all input fields.
When the buggy is edited and the flag pattern is 'Plain' the flag pattern gets deselected. There was a typo which was
found and solved.
* 2 bugs found
* 1 bugs solved

#### Test case 2: Modal pop-up
If the number of wheels is odd or the number of tyres is less than the number of wheels the editor should pop-up a modal to inform the user that the data is incorrect.
To check this, an odd number of wheels has been entered into the form and a pop-up modal was triggered when the 'Submit' button was pressed.
* 0 bugs found

#### Test case 3: Error message
To check if the appropriate message is on the modal a rule violation was made and when the modal was triggered the appropriate message was displayed to inform the user about the rule violation.
* 0 bugs found

#### Test case 4: Total cost
To check if the total cost of the buggy is correctly calculated a buggy has been created and the price was manually calculated and checked with the price calculated in the application.
The prices matched and this confirms that the price is correctly calculated.
* 0 bugs found

#### Test case 5: Json format
To check if the correct Json data is extracted, Json data format has been copied into notepad and compared with the data from the table.
The data was correct and the appropriate Json is extracted every time.
* 0 bugs found

### Total bugs observed: 2

#### Critical bugs: 0

#### Major bugs: 1

#### Minor bugs: 1


* Form page: If the user completes the form with the desired data and then the 'Autofill' button is pressed the form does not keep the manually entered data.
