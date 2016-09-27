package regist

import(
  "fmt"
  "net/http"
  _ "github.com/go-sql-driver/mysql"
  "database/sql"
  "log"
)

func (this *RegistInfo)Get(){
  fmt.Fprintf(this.Res,"reg get\n")
}

func (this *RegistInfo)Post(){
  //open database
  db,err:=sql.Open("mysql","toolman:marginal@tcp(127.0.0.1:3306)/Toolbox_product")
  checkerr(err)
  defer db.Close()

  //check account valid ?
  rows, err := db.Query("SELECT Account FROM logindata where Account = ?", this.Account)
  checkerr(err)
  defer rows.Close()
  var AccountValid bool =  true
  for rows.Next(){
    AccountValid = false
  }

  //check mail valid ?
  rows, err := db.Query("SELECT Mail FROM logindata where Mail = ?", this.Mail)
  checkerr(err)
  defer rows.Close()
  var MailValid bool =  true
  for rows.Next(){
    MailValid = false
  }

  //all okay -> mail confirmation
}

func checkerr(err error) {
  if err != nil {
    log.Fatal(err)
  }
}
