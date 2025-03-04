
import sqlite3
from weather_object import Weather
  
### Processing planes data
class Planes:
 
    def __init__(self, city):
        self.name = None
        self.weight = None
        self.planes = []
        self.planes_number = None
        self.create_db()
        self.read_db()
        self.weather = Weather(city)
        
    def create_db(self):
        try:
            conn = sqlite3.connect("models.db")
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS models (
                        id INTEGER, 
                        plane_name TEXT NOT NULL, 
                        plane_weight INTEGER NOT NULL,
                        PRIMARY KEY (id))""")
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return "Database error: {e}"    
        
    def read_db(self):     
        """ 
        - Reads the database and load into self.planes
        - Set the self.planes_number
        self.planes format will be a tuple within a list
        id,plane_name,plane_weight
        [(1, 'Sport Cub 500', 65), (3, 'BF 109', 400)]
        """
        
        
        try:       
            conn = sqlite3.connect('models.db')
            c = conn.cursor()
            res = c.execute("SELECT id, plane_name, plane_weight FROM models")
            self.planes = res.fetchall()
            self.planes_number = len(self.planes)
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            return "Database error: {e}"
            
            
    def add_plane(self, plane_and_weight):
        """ 
        Adds up to 5 planes to the database. 
        :param plane_and_weight: str"Super Cub 500,65"
        """
        
        try:
            if not self.planes_number >= 5:
                
                name, weight = plane_and_weight.split(",")
                new_id = (((int(self.planes[-1][0]))+1) if self.planes else 1)
                conn = sqlite3.connect('models.db')
                c = conn.cursor()
                c.execute("INSERT INTO models VALUES(?, ?, ?)", (new_id, name, int(weight)))
                conn.commit()
                conn.close()
                
                self.read_db()
                return "Successfully added"
                
            else:
                return "You have already 5 planes"
        except sqlite3.Error as e:
            return f"Database error: {e}"
    

    def remove_plane(self,id_or_name):          
        # :param id_or_name: ex: int"3" or str"super cub 500"
        
        try:
            conn = sqlite3.connect('models.db')
            c = conn.cursor()
            
            if str(id_or_name).isdigit():
                c.execute("DELETE FROM models WHERE id=(?)", (id_or_name,))
            else:
                c.execute("DELETE FROM models WHERE plane_name=(?)", (id_or_name,))
        
            conn.commit()
            conn.close()
            self.read_db()
            return "List updated"

        except sqlite3.Error as e:
            return f"Database error: {e}"
               
            
    def plane_name(self, plane_id):
    
        for plane in self.planes:
            if plane[0] == plane_id:
                return plane[1]
        else:
            return "Not valid plane"
        
        
    def plane_weight(self, plane_id):

        for plane in self.planes:
            if plane[0] == plane_id:
                return plane[2]
        else:
            return "Not valid plane"
        
        
    def get_planes_list(self):
        return [(f"{plane[0]} | {plane[1]} | {plane[2]}g") for plane in self.planes]
            
        
    def flight_circumstances(self, plane_id=0, current_or_hourly="current", predict_hours=0): 
        """
        Returns the flight circumstances of the given id plane. If there is a bad weather outside than that.
        e.g. "What could go wrong?", "Snow out there!"
        
        :arguments:
        plane_id=1-5 (chooses the plane from csv)
        current_or_hourly="current" or "hourly"
        predict_hours= n, only needed when your current_or_hourly is "hourly", default is 0
        in use: 3, 6, 9 
        """
        
        wind_speed = 0
        weight = 0
        good_weather_condition = ("clear sky", "few clouds", "scattered clouds", "broken clouds", "overcast clouds", "light intensity drizzle", "light rain", "light snow", "mist", "smoke", "sand", "dust")
        
        for plane in self.planes:
            if plane[0] == plane_id:
                weight = int(plane[2])
                break
        else:
            return "Not valid plane"
        
        
        if current_or_hourly == "current":
            data = self.weather.get_weather_current()
        elif current_or_hourly == "hourly":
            data = self.weather.get_weather_hourly(predict_hours) # vagy előbb wind változóba menteni és ugy lekérni
            predict_hours -= 1
        else:
            return "Not valid state"
        
        
        
        if data[predict_hours][4] not in good_weather_condition:
                return f"{data[predict_hours][4].capitalize()} out there!"   

        wind_speed = float(data[predict_hours][1])
        
        if 0 < weight < 200:
            wind_multiplier = 1.4
        elif 200 <= weight <= 1000:
            wind_multiplier = 1.2
        elif 1000 < weight <= 2000:
            wind_multiplier = 1.0
        else:
            wind_multiplier = 0.8

        adjusted_wind = wind_speed * wind_multiplier

       
        if adjusted_wind <= 6:
            return "Perfect flight conditions"
        elif 6 < adjusted_wind <= 11:
            return "Perfect for practice"
        elif 11 < adjusted_wind <= 16:
            return "Challangeing circumstances"
        elif 16 < adjusted_wind <= 22:
            return "What could go wrong?"
        else:
            return "Will be expensive. Very Risky"
        
        
if __name__ == '__main__':
    planes = Planes("Iceland")
    print(planes.add_plane("BF 111, 450"))
    print(planes.add_plane("BF 109, 400"))
    # # print(planes.remove_plane(1))
    # print(planes.planes)
    # print(planes.planes_number)
    # print(planes.plane_name(3))
    # print(planes.plane_weight(3))
    print(planes.get_planes_list())
    # print(planes.flight_circumstances(plane_id=3, current_or_hourly="current", predict_hours=0))