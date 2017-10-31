# webAppGoogle
Utilitarian web app using google cloud platform

## TODOs
- Add Login and Logout: <br />
https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql-part-2--cms-22999  <br />
https://cloud.google.com/appengine/docs/standard/python/authenticating-users-firebase-appengine

- Be able to upload images: <br />
https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql-part-6--cms-23402

- Scheduling tasks for daily Bulletin update: <br />
https://cloud.google.com/appengine/docs/standard/python/config/cron

- Send Emails from python in Google App Engine: <br />
https://cloud.google.com/appengine/docs/standard/python/mail/

- Python scripts to retreive/parse information from Bulletin and parse it <br />
https://stackoverflow.com/questions/33566843/how-to-extract-text-from-html-page
https://www.crummy.com/software/BeautifulSoup/ <br />
https://www.crummy.com/software/BeautifulSoup/bs4/doc/ <br />

- Add Facebook Login: <br />
https://developers.facebook.com/docs/facebook-login/android/

- Add Android interface and Push Notifications : <br />
https://cloud.google.com/solutions/mobile/firebase-app-engine-android-studio

- Enable payments: <br />
https://stackoverflow.com/questions/6092626/how-to-integrate-payment-processing-with-gwt-gae-based-app <br />
https://stripe.com/  <br />
https://github.com/petertodd/python-bitcoinlib

- Add Multilanguage: <br />
https://pythonhosted.org/Flask-Babel/

- Research security voulnerabilities of Flask or things in general: <br />
https://nvisium.com/blog/2015/12/07/injecting-flask/

- Case insensitive query: <br />
https://stackoverflow.com/questions/16082575/sql-ignore-case-while-searching-for-a-string  <br />
https://alvinalexander.com/sql/sql-select-case-insensitive-query-queries-upper-lower

## Functions
- info getBoletinDiaActual(zona): busca boletin publicado en las ultimas 24 horas. (Scheduling tasks)

- info searchBoletinDiaActual(criterios de busqueda por definir): busca cadena, nombre, numero, etc dependiendo cual sea el criterio de busqueda, en el boletin del dia actual. (Query on Local/own database)

- mailBoletin(boletin): enviar al email del usuario registrado la informacion de la busqueda 

- getBoletinesHistorico(zona,fromDay,fromMonth,fromYear,toDay,toMonth,toYear): funcion que busca todos los boletines especificados dentro del rango de fechas por zona. (Admin only)

