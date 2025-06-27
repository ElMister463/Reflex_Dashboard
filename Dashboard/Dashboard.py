import reflex as rx
from collections import Counter

class User( rx.Base ):
     name : str
     email : str
     gender : str

class State( rx.State ):

     users: list[ User ] = []
     users_for_graph: list[ dict ] = []

     def add_user( self, form_data: dict ):
          self.users.append( User( **form_data ) )
          self.transform_data()

     def transform_data( self ):
          gender_counts = Counter(
               user.gender for user in self.users
          )

          self.users_for_graph = [
               { "name" : gender_group, 
                 "value" : count }

                 for gender_group, count in gender_counts.items()
          ]
         

def show_user( user: User ) -> rx.Component:
     return rx.table.row(
          rx.table.cell( user.name ),
          rx.table.cell( user.email ),
          rx.table.cell( user.gender ),

          style = { "_hover": { "bg": rx.color( "gray", 3) } },
          align = "center",

     )


def add_customer_button() -> rx.Component:
     return rx.dialog.root(
          rx.dialog.trigger(
               rx.button(
                    rx.icon( "plus",
                            size = 26 ),
                            rx.text( "Add user",
                                    size = "4" ),
               ),
          ),
     
          rx.dialog.content(
               rx.dialog.title(
                    "Add New User",
               ),
               rx.dialog.description(
                    "Fill the form with the user's info.",
               ),
               rx.form(
                    rx.flex(
                         rx.input(
                              placeholder = "User name",
                              name = "name",
                              required = True,
                         ),
                         rx.input(
                              placeholder = "user@example.com",
                              name = "email",
                              required = True,
                         ),
                         rx.select(
                              [ "Male", "Female" ],
                              placeholder = "Male",
                              name = "gender",
                              required = True
                         ),
                         rx.flex(
                              rx.dialog.close(
                                   rx.button(
                                        "Cancel",
                                        variant = "soft",
                                        color_scheme = "gray",
                                   ),
                              ),
                              rx.dialog.close(
                                   rx.button(
                                        "Submit",
                                        type = "submit",
                                   ),
                              ),

                              spacing = "3",
                              justify = "end",
                         ),

                         direction = "column",
                         spacing = "4",
                    ),

                    on_submit = State.add_user,
                    reset_on_submit = False,
               ),

               max_width = "450px",
             
          ),

     )


def graph():
     return rx.recharts.bar_chart(
          rx.recharts.bar(
               data_key = "value",
               stroke = rx.color( "accent", 9 ),
               fill = rx.color( "accent", 8),
          ),
          rx.recharts.x_axis( data_key = "name" ),
          rx.recharts.y_axis(),
          data = State.users_for_graph,
          width = "50%",
          height = 250,
     )



def index() -> rx.Component:
    return rx.center(
          rx.vstack(
               add_customer_button(),
               rx.table.root(
                    rx.table.header(
                         rx.table.row(
                              rx.table.column_header_cell( "Name" ),
                              rx.table.column_header_cell( "Email" ),
                              rx.table.column_header_cell( "Gender" ),  
                         ),
                    ),
                    rx.table.body(
                         rx.foreach( State.users, 
                                   show_user ),
                    ),
               variant = "surface",
               size = "3"
               ),

               graph(),
               align = "center",
               spacing = "5",
               width = "100%",
               
    ),

     width="100vw",  
     height="100vh",
    )
    

app = rx.App(
     theme = rx.theme( 
          radius = "full",
          accent_color = "red",
     )
)
app.add_page( 
     index,
     title = "Dashboard App",
     description = "A simple dashboard app",
     on_load = State.transform_data,
 )