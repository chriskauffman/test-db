from sqlobject import connectionForURI, SQLObject, UuidCol

from uuid import UUID, uuid4


class ObjectWithUuid(SQLObject):
    uid: UuidCol = UuidCol(alternateID=True, default=None)


connection = connectionForURI("sqlite:UuidCol_alternateID.sqlite")
ObjectWithUuid.createTable(connection=connection, ifNotExists=True)


test_object = ObjectWithUuid(
    uid=uuid4(),
    connection=connection,
)

# This confirms that we have a UUID
print(isinstance(test_object.uid, UUID))

# Shouldn't this work?
print(ObjectWithUuid.byUid(test_object.uid, connection=connection))

# Shouldn't this return True?
print((ObjectWithUuid.byUid(test_object.uid, connection=connection) is test_object))

# Shouldn't this also work?
print(
    (ObjectWithUuid.byUid(str(test_object.uid), connection=connection) is test_object)
)


test_uuid = uuid4()

test_object = ObjectWithUuid(
    uid=test_uuid,
    connection=connection,
)

# This confirms that we have a UUID
print(isinstance(test_uuid, UUID))
print(isinstance(test_object.uid, UUID))
print((test_object.uid == test_uuid))

# Shouldn't this work?
print(ObjectWithUuid.byUid(test_uuid, connection=connection))
# results in formencode.api.Invalid: expected uuid in the UuidCol 'uid', got <class 'str'> 'dd6a3940-b075-4ef0-9940-da2024499cf1' instead

# Shouldn't this return True?
print((ObjectWithUuid.byUid(test_uuid, connection=connection) is test_object))

# Shouldn't this also work?
print((ObjectWithUuid.byUid(str(test_uuid), connection=connection) is test_object))
