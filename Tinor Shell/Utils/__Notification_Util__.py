from winotify import Notification
  

def Error_Notification():

    Notify = Notification(app_id="Tinor Shell",
                        title="An error has occurred!",
                        msg="In a Command or program ran using Tinor Shell there has been a Error",
                        
                        )

    Notify.show()
