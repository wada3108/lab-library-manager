<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>ユーザ情報 - 研究室 蔵書管理システム</title>
        <link rel = "stylesheet" href = "/static/style.css">
        <link rel = "stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0" />
    </head>

    <header class = "header">
        <div class = "spacer"></div>
        <h1>研究室 蔵書管理システム</h1>
        <div class = "accountmenu">
            <a class = "account" href = "">
                <span class="material-symbols-outlined">
                    account_circle
                </span>
                ログイン中
            </a>
            <ul class = "dropdown">
                <li>{{uname}}さん</li>
                <li><a href = "user?id={{uid}}">ユーザ情報</a></li>
                <li><a href = "logout">ログアウト</a></li>
            </ul>
        </div>
    </header>

    <nav id = "gnavi">
        <ul>
            <li><a href = "index">ホーム</a></li>
            <li><a href = "uall">一覧・貸出・予約</a></li>
            <li><a href = "usearch">検索・貸出・予約</a></li>
            <li><a href = "return">返却</a></li>
            <li><a href = "cancel">予約管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>ユーザ情報変更</h2>
                <p>
                    変更したい項目にチェックをつけ、変更したい内容を入力してください。<br>
                    なお、半角英数以外の文字とスペースは利用できないのでご注意ください。<br>
                    また、パスワードを変更する場合は、現在のパスワード、新しいパスワード、新しいパスワード(確認用)の3項目全てを入力してください。
                </p>
                <p class = "error">{{errormsg}}</p>
                <form method = "POST" class = "form">
                    <dl>
                        <dt>変更する項目</dt>
                        <dd>
                            %if "name" in item:
                                <input type = "checkbox" name = "item" value = "name" checked>ユーザ名
                            %else:
                                <input type = "checkbox" name = "item" value = "name">ユーザ名
                            %end
                            %if "email" in item:
                                <input type = "checkbox" name = "item" value = "email" checked>メールアドレス
                            %else:
                                <input type = "checkbox" name = "item" value = "email">メールアドレス
                            %end
                            %if "password" in item:
                                <input type = "checkbox" name = "item" value = "password" checked>パスワード
                            %else:
                                <input type = "checkbox" name = "item" value = "password">パスワード
                            %end
                        </dd>              
                    </dl>
                    <dl>
                        <dt>ユーザ名</dt>
                        <dd><input type = "text" name = "name" value = {{data[0]}}></dd>
                        <dt>メールアドレス</dt>
                        <dd><input type = "email" name = "email" value = {{data[1]}}></dd>
                        <dt>現在のパスワード<br>新しいパスワード<br>新しいパスワード(確認用)</dt>
                        <dd>
                            <input type = "password" name = "currentpassword" class = "pw" value = {{data[2]}}><br>
                            <input type = "password" name = "newpassword" class = "pw" value = {{data[3]}}><br>
                            <input type = "password" name = "newpassword2" class = "pw" value = {{data[4]}}></dd>
                    </dl>
                    <p id = "sendbuttoncover">
                        <input type = "submit" value = "変更" id = "sendbutton" formaction = "uchange?id={{id}}">
                        <input type = "submit" value = "取消" id = "modifybutton" formaction = "uchange?id={{id}}&cancel=True">
                    </p>
                </form>            
        </div>
    </body>
    <footer>
        <small class = "fsmall">
            Copyright &copy; 2022 WADA Towa All rights reserved.
        </small>    
    </footer>
</html>