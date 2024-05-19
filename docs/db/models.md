    Table Transactions {
      id int
      currency_id int
      type varchar
      created_at timestamp 
      modified_at timestamp
    }
    
    Table TransactionBills {
      id int
      transaction_id int
      bill_id int
      quantity int
      created_at timestamp 
      modified_at timestamp
    
    }
    
    Table Currencies {
      id int
      name varchar 
    }
    
    
    Table Bills {
      id int
      currency_id int 
      value int
    }
    
    Table BankBills {
      id int
      bills_id int 
      quantity int
    }
    
    Ref: Bills.currency_id > Currencies.id // many-to-one
    Ref: BankBills.bills_id > Bills.id
    Ref: TransactionBills.transaction_id > Transactions.id
    Ref: TransactionBills.bill_id > Bills.id
    REf: Transactions.currency_id > Currencies.id




https://dbdiagram.io/d