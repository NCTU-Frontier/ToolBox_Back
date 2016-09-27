package main

import(
  "net/gttp"
  "log"
  "html/template"
)

func main(){
  http.HandleFunc("",)
  err:=http.ListenAndServe(":80",nil)
  if err!=nil{
    log.Fatal("ListenAndServe: ",err)
  }
}
