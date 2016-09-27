package regist

import(
  "~/toolbox/pkg/user"
  "net/http"
)

func RegistInfo struct{
  UserInfo
  Res       http.ResponseWriter
  Req       *http.Request
}

func RegistHandle(res http.ResponseWriter, req *http.Request){
  req.ParseForm()

  //Initialization
  var this RegistInfo
  this.Name=req.Form["Name"]
  this.Account=req.Form["Account"]
  this.Password=req.Form["Mail"]
  this.Birth=req.Form["Birth"]
  this.Res=res
  this.Req=req

  if req.Method=="GET"{
    (&this).Get()
  }else if req.Method=="POST"{
    (&this).Post()
  }
}
