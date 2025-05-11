<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>ログイン - 研究室 蔵書管理システム</title>
        <link rel = "stylesheet" href = "/static/style.css">
    </head>
    <div class="loginform-wrapper">
        <h1>研究室 蔵書管理システム</h1>
        %if error[0] == "":
        <div class = "hidden">
        %end
        <p class = "loginerror">
            <span class = "bold">{{error[0]}}</span>
            <br>
            {{error[1]}}
        <p>
        %if error[0] == "":
        </div>
        %end
        <form method = "POST" action = "dologin?prev={{prev}}">
            <input type="text" name="name" class = "logininput"required="required" placeholder="ユーザ名"></input>        
            <input type="password" name="password" class = "logininput" required="required" placeholder="パスワード"></input>
            <p class = "sendbuttoncover">
                <input type = "submit" id = "sendbutton" value = "ログイン"></input>
            </p>
        </form>
    </div>
</html>