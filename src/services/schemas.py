from marshmallow import Schema


class PhotoSchema(Schema):
    class Meta:
        fields = ('uuid', 'url', 'status', 'created_at')

photo_serializer = PhotoSchema()
photos_serializer = PhotoSchema(many=True)
