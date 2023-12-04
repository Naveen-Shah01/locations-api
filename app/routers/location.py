from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException,status,Response,Depends,APIRouter
from ..import models,schemas,oauth2
from ..database import get_db
from typing import List


# @app.post("/add_location", status_code=status.HTTP_201_CREATED)
# def add_location(location: CreateLocation):
#     print(location)
#     cursor.execute("""INSERT INTO locationdata ("longitude", "latitude", "name","description") VALUES (%s,%s,%s,%s) RETURNING * """,
#                    (location.longitude,location.latitude,location.name,location.description))
#     new_location = cursor.fetchone()
#     # Make the changes to the database persistent
#     conn.commit()
#     print(new_location)
#     return {
#         "Data": new_location
#     }

router = APIRouter(
    tags=['Location']
)

@router.post("/add_location", status_code=status.HTTP_201_CREATED,response_model=schemas.LocationResponse)
def add_location(location: schemas.LocationCreate,db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user)):
    print(location)
    print(current_user.id)
    # new_location = models.Location(longitude=location.longitude,latitude=location.latitude,
    #                 name=location.name,description=location.description)
    new_location = models.Location(owner_id = current_user.id,**location.model_dump())

    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return  new_location




# @app.get("/get_location")
# def get_location():
#     cursor.execute("""SELECT*FROM locationdata; """)
#     locations = cursor.fetchall()
#     print(locations)
#     return {
#         "Data": locations
#     }

# @router.get("/get_location",response_model=List[schemas.LocationResponse])
@router.get("/get_location")
def get_location(db: Session = Depends(get_db), limit:int=50):
    # limit is for pagination 
    locations = db.query(models.Location).limit(limit).all()
    # results = db.query(models.Location,models.User.email).join(models.User,models.Location.owner_id==models.User.id).all()
    # print(results)
    return locations

  

# To delete the location by id
# @app.delete("/delete_location/{locationId}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_location(locationId:int):
#     print(locationId)
#     cursor.execute("""DELETE FROM locationdata WHERE locationid = %s RETURNING * """,
#                    (str(locationId),))
#     deleted_location = cursor.fetchone()
#     print("deleted_location")
#     conn.commit()
#     if deleted_location == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Location with id: {locationId} does not exist")
#     return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.delete("/delete_location/{locationId}",status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id:int,db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user)):
    print(location_id)
    location = db.query(models.Location).filter(models.Location.locationid == location_id)
    if location.first() == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location with id: {location_id} does not exist")
    location.delete(synchronize_session=False)
    db.commit()
    print("deleted_location")
    return Response(status_code = status.HTTP_204_NO_CONTENT)




# To update the location
# @app.put("/update_location/{locationId}",status_code=status.HTTP_200_OK)
# def update_location(locationid:int,location:CreateLocation):
#     print(locationid)
#     cursor.execute("""UPDATE locationdata SET longitude=%s, latitude = %s, name = %s, description=%s 
#                    WHERE locationid = %s RETURNING * """,
#                    (location.longitude,location.latitude,location.name,location.description,str(locationid)))
#     updated_location = cursor.fetchone()
#     print("updated_location")
#     conn.commit()
#     if updated_location == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Location with id: {locationid} does not exist")
#     return {"data":updated_location}
    

@router.put("/update_location/{locationId}",status_code=status.HTTP_200_OK,response_model=schemas.LocationResponse)
def update_location(location_id: int, location: schemas.LocationCreate, db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user)):
    print(location_id)
    location_query = db.query(models.Location).filter(models.Location.locationid == location_id)
    updated_location = location_query.first()

    if updated_location == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location with id: {location_id} does not exist")
    
    location_query.update(location.model_dump(),synchronize_session=False)
    db.commit()
    print("Location updatded sucessfully")
    return location_query.first()






