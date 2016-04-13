
# 1 Overview 

The aim of the CoÐoo transaction engine is to get a kind of multipurpose module to cover many aspects toward the use of Community / Crypto Currencies in Odoo.
 
Beside to serve as future inside Odoo transaction engine it is planned to add a simulation module, that enables to simulate the full range of different kind of community currencies inside CoÐoo Exchange. Another very interesting feature is that it can be used as wallet to run external transactions engines as Bitcoin/Ethereum or Eris for instance.
Here a not yet complete list of different possible usecases:
 

1.  Rapid prototyping for currency systems, to get feedback 
    and improve
    
2.  Simulation tool which enables to run tests on
    different kind of community or corporate currencies

3.  Basic of a Odoo integrated wallet for distributed ledgers and smart-contracts
 

> Note:
> The existent transaction engine of Vertical Community was not flexible enough on the one hand and on the other complex, because it was completely integrated into the Odoo accounting system. 
Out of this reason we started to refactor the code into a more straightforward solution and used the new ORM API for it. The specification are build upon this refactored transaction engine called
> Vertical Exchange.

<span id="a_2_Specifications"> 2 Specifications
=================================================================================================

 
This are some draft specification to help developers to get a quick overview about the CoÐoo Exchange framework.

 

<span id="a_2_1_Vertical_Exchange"> 2.1 Vertical Exchange
-----------------------------------------------------------------------------------------------------------

Vertical Exchange contains about six Odoo modules, some of them are more or less untouched copied from Vertical Community, some contain quite new code.

To avoid compliance problem the whole set of modules from Vertical Community has been forked into two new projects Vertical Exchange” and “Vertical Community2”.

Vertical Community2 contains all modules that are not related to Exchange or Marketplace. The Vertical Exchange project contains the Exchange and Marketplace Modules. 

 

### <span id="a_2_1_1_Basic_Data_Model"> 2.1.1 Basic Data Model 

The Basic Data Model is very flexible and extensible to future needs. It is built analogue of the Cyclos 3.6 transaction engine model.


![Basic Specifications models](img/Basic_Specifications_models.png)
 
 
Beside of \*res.currency and res.partner also others standard models of Odoo are accessed, but this are the most important.

An addition model id distributed\_db what contains settings for attaching an external ledger or any DB distributed or not.

A more detailed data model is accessible here:

<https://github.com/codoo/vertical-exchange/docs/dev>


### <span id="a_2_1_2_Functionality">2.1.2 Functionality

The easiest way to explain the functionality is according some screenshots:

![Exchange Transactions-Odoo](img/Exchange-Settings-Odoo.png)



### <span id="a_2_1_3_Settings"> 2.1.3 Settings

We see in the accounts section <span class="T25">three </span>type of
accounts, one for member Member and two System
accounts. A System Account is a single account that belongs to the System or organisation. Member accounts are templates for the member that are in a group of membership. Membership is a function of the Odoo Association app.

Each account can have a currency and could theoretically use an outside transaction engine.

The settings, as any other model, can easily extended via the
inheritance function Odoo.



Consequently the settings for each account type look looks as this
example.

 

<img src="img/Exchange-Transactions-Odoo.png" width="400">

Related account is the account of the Odoo accounting system. This
option allows the integration of an exchange into the accounting system.


When you click on External DB a new field appears where you can open the
settings for External DB's.

 
### <span id="a_2_1_4_Transactions">2.1.4 Transactions 

Transaction are performed as following scheme shows.

 
![Basic Specifications models](img/Basic_Specifications_transaction.png)
 
 

For a transaction type it is also possible to ad one
or more follow up transaction, for example to charge transaction
fees.

### <span id="a_2_1_5_Transaction">2.1.5 Transaction Workflow

The Workflow of transaction is designed accord the following Business Process sheet:

![Exchange Transaction - Workflow](img/CoDoo_Framework_workflow_1.png)
  
The process has to two lanes one for direct payments and one for Invoiced payments. If the transaction is performed over the internal Odoo transaction engine the process is going immediately from "sent" to "paid". If the transaction engine of one of the accounts is outside Odoo (external DB) the process is waiting for approval that the transaction has successfully taken place.

In Odoo itself the same workflow looks as this sheet:

![Transaction - Odoo Workflow](img/TransactionWorkflow1-Odoo.png) 
  
The transition trigger are showed in the first line and the conditions for that transition in the second.
For example "do_payment" is the name of the "Send Payment" button and "test_access_role..." is to check if the user has the right to perform this step.   