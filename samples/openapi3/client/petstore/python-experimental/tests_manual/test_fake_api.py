# coding: utf-8

"""
    OpenAPI Petstore

    This spec is mainly for testing Petstore server and contains fake endpoints, models. Please do not use this for any other purpose. Special characters: \" \\  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""
from email.mime import multipart
from email.mime import nonmultipart
import io
import sys
import unittest
import json
import typing
from unittest.mock import patch

import urllib3
from urllib3._collections import HTTPHeaderDict

import petstore_api
from petstore_api import api_client, schemas, exceptions
from petstore_api.api.fake_api import FakeApi  # noqa: E501
from petstore_api.rest import RESTClientObject


class MIMEFormdata(nonmultipart.MIMENonMultipart):
    def __init__(self, keyname, *args, **kwargs):
        super(MIMEFormdata, self).__init__(*args, **kwargs)
        self.add_header(
            "Content-Disposition", "form-data; name=\"%s\"" % keyname)


class TestFakeApi(unittest.TestCase):
    """FakeApi unit test stubs"""
    json_content_type = 'application/json'
    configuration = petstore_api.Configuration()
    api = FakeApi(api_client=api_client.ApiClient(configuration=configuration))

    @staticmethod
    def headers_for_content_type(content_type: str) -> dict[str, str]:
        return {'content-type': content_type}

    @classmethod
    def __response(
        cls,
        body: typing.Union[str, bytes],
        status: int = 200,
        content_type: str = json_content_type,
        headers: typing.Optional[dict[str, str]] = None,
        preload_content: bool = True
    ) -> urllib3.HTTPResponse:
        if headers is None:
            headers = {}
        headers.update(cls.headers_for_content_type(content_type))
        return urllib3.HTTPResponse(
            body,
            headers=headers,
            status=status,
            preload_content=preload_content
        )

    @staticmethod
    def __json_bytes(in_data: typing.Any) -> bytes:
        return json.dumps(in_data, separators=(",", ":"), ensure_ascii=False).encode('utf-8')

    @staticmethod
    def __assert_request_called_with(
        mock_request,
        url: str,
        method: str = 'POST',
        body: typing.Optional[bytes] = None,
        content_type: typing.Optional[str] = 'application/json',
        fields: typing.Optional[tuple[api_client.RequestField, ...]] = None,
        accept_content_type: str = 'application/json',
        stream: bool = False,
        query_params: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None
    ):
        headers = {
            'Accept': accept_content_type,
            'User-Agent': 'OpenAPI-Generator/1.0.0/python'
        }
        if content_type:
            headers['Content-Type'] = content_type
        kwargs = dict(
            headers=HTTPHeaderDict(headers),
            query_params=query_params,
            fields=fields,
            stream=stream,
            timeout=None,
        )
        if method != 'GET':
            kwargs['body'] = body
        mock_request.assert_called_with(
            method,
            url,
            **kwargs
        )

    def test_array_model(self):
        from petstore_api.model import animal_farm, animal

        # serialization + deserialization works
        with patch.object(RESTClientObject, 'request') as mock_request:
            json_data = [{"className": "Cat", "color": "black"}]
            mock_request.return_value = self.__response(
                self.__json_bytes(json_data)
            )

            cat = animal.Animal(className="Cat", color="black")
            body = animal_farm.AnimalFarm([cat])
            api_response = self.api.array_model(body=body)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/refs/arraymodel',
                body=self.__json_bytes(json_data)
            )

            assert isinstance(api_response.body, animal_farm.AnimalFarm)
            assert api_response.body == body

    def test_recursionlimit(self):
        """Test case for recursionlimit

        """
        assert sys.getrecursionlimit() == 1234

    def test_array_of_enums(self):
        from petstore_api.model import array_of_enums, string_enum

        # serialization + deserialization works
        with patch.object(RESTClientObject, 'request') as mock_request:
            value = [string_enum.StringEnum("placed")]
            body = array_of_enums.ArrayOfEnums(value)
            value_simple = ["placed"]
            mock_request.return_value = self.__response(
                self.__json_bytes(value_simple)
            )

            api_response = self.api.array_of_enums(body=body)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/refs/array-of-enums',
                body=self.__json_bytes(value_simple)
            )

            assert isinstance(api_response.body, array_of_enums.ArrayOfEnums)
            assert api_response.body == body

    def test_number_with_validations(self):
        from petstore_api.model import number_with_validations

        # serialization + deserialization works
        with patch.object(RESTClientObject, 'request') as mock_request:
            value = 10.0
            body = number_with_validations.NumberWithValidations(value)
            mock_request.return_value = self.__response(
                self.__json_bytes(value)
            )

            api_response = self.api.number_with_validations(body=body)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/refs/number',
                body=self.__json_bytes(value)
            )

            assert isinstance(api_response.body, number_with_validations.NumberWithValidations)
            assert api_response.body == value

    def test_composed_one_of_different_types(self):
        from petstore_api.model import composed_one_of_different_types

        # serialization + deserialization works
        number = composed_one_of_different_types.ComposedOneOfDifferentTypes(10.0)
        cat = composed_one_of_different_types.ComposedOneOfDifferentTypes(
            className="Cat", color="black"
        )
        none_instance = composed_one_of_different_types.ComposedOneOfDifferentTypes(None)
        date_instance = composed_one_of_different_types.ComposedOneOfDifferentTypes('1970-01-01')
        cast_to_simple_value = [
            (number, 10.0),
            (cat, {"className": "Cat", "color": "black"}),
            (none_instance, None),
            (date_instance, '1970-01-01'),
        ]
        for (body, value_simple) in cast_to_simple_value:
            with patch.object(RESTClientObject, 'request') as mock_request:
                mock_request.return_value = self.__response(
                    self.__json_bytes(value_simple)
                )

                api_response = self.api.composed_one_of_different_types(body=body)
                self.__assert_request_called_with(
                    mock_request,
                    'http://petstore.swagger.io:80/v2/fake/refs/composed_one_of_number_with_validations',
                    body=self.__json_bytes(value_simple)
                )

                assert isinstance(api_response.body, composed_one_of_different_types.ComposedOneOfDifferentTypes)
                assert api_response.body == body

        # inputting the uncast values into the endpoint also works
        for (body, value_simple) in cast_to_simple_value:
            with patch.object(RESTClientObject, 'request') as mock_request:
                mock_request.return_value = self.__response(
                    self.__json_bytes(value_simple)
                )

                api_response = self.api.composed_one_of_different_types(body=value_simple)
                self.__assert_request_called_with(
                    mock_request,
                    'http://petstore.swagger.io:80/v2/fake/refs/composed_one_of_number_with_validations',
                    body=self.__json_bytes(value_simple)
                )

                assert isinstance(api_response.body, composed_one_of_different_types.ComposedOneOfDifferentTypes)
                assert api_response.body == body

    def test_string(self):
        # serialization + deserialization works
        with patch.object(RESTClientObject, 'request') as mock_request:
            body = "blah"
            value_simple = body
            mock_request.return_value = self.__response(
                self.__json_bytes(value_simple)
            )

            api_response = self.api.string(body=body)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/refs/string',
                body=self.__json_bytes(value_simple)
            )

            assert isinstance(api_response.body, str)
            assert api_response.body == value_simple

    def test_string_enum(self):
        from petstore_api.model import string_enum
        # serialization + deserialization works
        with patch.object(RESTClientObject, 'request') as mock_request:
            value = "placed"
            body = string_enum.StringEnum(value)
            mock_request.return_value = self.__response(
                self.__json_bytes(value)
            )

            api_response = self.api.string_enum(body=body)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/refs/enum',
                body=self.__json_bytes(value)
            )

            assert isinstance(api_response.body, string_enum.StringEnum)
            assert api_response.body == value

    def test_mammal(self):
        # serialization + deserialization works
        from petstore_api.model.mammal import Mammal
        with patch.object(RESTClientObject, 'request') as mock_request:
            body = Mammal(className="BasquePig")
            value_simple = dict(className='BasquePig')
            mock_request.return_value = self.__response(
                self.__json_bytes(value_simple)
            )

            api_response = self.api.mammal(body=body)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/refs/mammal',
                body=self.__json_bytes(value_simple)
            )

            assert isinstance(api_response.body, Mammal)
            assert api_response.body == value_simple

    def test_missing_or_unset_required_body(self):
        # missing required body
        with self.assertRaises(TypeError):
            self.api.mammal()
        # required body may not be unset
        with self.assertRaises(petstore_api.ApiValueError):
            self.api.mammal(body=schemas.unset)

    def test_missing_or_unset_required_query_parameter(self):
        from petstore_api.model.user import User
        user = User({})
        # missing required query param
        with self.assertRaises(petstore_api.ApiTypeError):
            self.api.body_with_query_params(body=user)
        # required query param may not be unset
        with self.assertRaises(petstore_api.ApiValueError):
            self.api.body_with_query_params(body=schemas.unset, query_params=dict(query=schemas.unset))

    def test_upload_download_file_tx_bytes_and_file(self):
        """Test case for upload_download_file
        uploads a file and downloads a file using application/octet-stream  # noqa: E501
        """
        import os
        test_file_dir = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "..", "testfiles"))
        file_name = '1px_pic1.png'
        file_path1 = os.path.join(test_file_dir, file_name)

        with open(file_path1, "rb") as some_file:
            file_bytes = some_file.read()
        file1 = open(file_path1, "rb")
        mock_response = self.__response(
            file_bytes,
            content_type='application/octet-stream'
        )
        try:
            with patch.object(RESTClientObject, 'request') as mock_request:
                mock_request.return_value = mock_response
                api_response = self.api.upload_download_file(body=file1)
                self.__assert_request_called_with(
                    mock_request,
                    'http://petstore.swagger.io:80/v2/fake/uploadDownloadFile',
                    body=file_bytes,
                    content_type='application/octet-stream',
                    accept_content_type='application/octet-stream'
                )
                self.assertTrue(isinstance(api_response.body, schemas.BinarySchema))
                self.assertTrue(isinstance(api_response.body, schemas.BytesSchema))
                self.assertTrue(isinstance(api_response.body, bytes))
                self.assertEqual(api_response.body, file_bytes)
        except petstore_api.ApiException as e:
            self.fail("upload_file() raised {0} unexpectedly".format(type(e)))
        finally:
            file1.close()

        # sending just bytes works also
        with patch.object(RESTClientObject, 'request') as mock_request:
            mock_request.return_value = mock_response
            api_response = self.api.upload_download_file(body=file_bytes)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/uploadDownloadFile',
                body=file_bytes,
                content_type='application/octet-stream',
                accept_content_type='application/octet-stream'
            )
            self.assertEqual(api_response.body, file_bytes)

    def test_upload_download_file_rx_file(self):
        import os
        test_file_dir = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "..", "testfiles"))
        file_name = '1px_pic1.png'
        file_path1 = os.path.join(test_file_dir, file_name)

        with open(file_path1, "rb") as some_file:
            file_bytes = some_file.read()

        # passing in file1 as the response body simulates a streamed response
        file1 = open(file_path1, "rb")

        class StreamableBody:
            """
            This class simulates http.client.HTTPResponse for a streamable response
            """
            def __init__(self, file: io.BufferedReader):
                self.fp = file

            def read(self, *args, **kwargs):
                return self.fp.read(*args, **kwargs)

            def close(self):
                self.fp.close()

        streamable_body = StreamableBody(file1)

        mock_response = self.__response(
            streamable_body,
            content_type='application/octet-stream',
            preload_content=False
        )
        with patch.object(RESTClientObject, 'request') as mock_request:
            mock_request.return_value = mock_response
            api_response = self.api.upload_download_file(body=file_bytes, stream=True)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/uploadDownloadFile',
                body=file_bytes,
                content_type='application/octet-stream',
                accept_content_type='application/octet-stream',
                stream=True
            )
        self.assertTrue(file1.closed)
        self.assertTrue(isinstance(api_response.body, schemas.BinarySchema))
        self.assertTrue(isinstance(api_response.body, schemas.FileSchema))
        self.assertTrue(isinstance(api_response.body, schemas.FileIO))
        self.assertEqual(api_response.body.read(), file_bytes)
        api_response.body.close()
        os.unlink(api_response.body.name)

        file1 = open(file_path1, "rb")
        streamable_body = StreamableBody(file1)
        saved_file_name = "fileName.abc"

        """
        when streaming is used and the response contains the content disposition header with a filename
        that filename is used when saving the file locally
        """
        mock_response = self.__response(
            streamable_body,
            content_type='application/octet-stream',
            headers={'content-disposition': f'attachment; filename="{saved_file_name}"'},
            preload_content=False
        )
        with patch.object(RESTClientObject, 'request') as mock_request:
            mock_request.return_value = mock_response
            api_response = self.api.upload_download_file(body=file_bytes, stream=True)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/uploadDownloadFile',
                body=file_bytes,
                content_type='application/octet-stream',
                accept_content_type='application/octet-stream',
                stream=True
            )
        self.assertTrue(file1.closed)
        self.assertTrue(isinstance(api_response.body, schemas.BinarySchema))
        self.assertTrue(isinstance(api_response.body, schemas.FileSchema))
        self.assertTrue(isinstance(api_response.body, schemas.FileIO))
        self.assertTrue(api_response.body.name.endswith(saved_file_name))
        self.assertEqual(api_response.body.read(), file_bytes)
        api_response.body.close()
        os.unlink(api_response.body.name)

    def test_upload_file(self):
        """Test case for upload_file
        uploads a file using multipart/form-data  # noqa: E501
        """
        import os
        test_file_dir = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "..", "testfiles"))
        file_name = '1px_pic1.png'
        file_path1 = os.path.join(test_file_dir, file_name)

        with open(file_path1, "rb") as some_file:
            file_bytes = some_file.read()
        file1 = open(file_path1, "rb")
        response_json = {
            'code': 200,
            'type': 'blah',
            'message': 'file upload succeeded'
        }
        try:
            with patch.object(RESTClientObject, 'request') as mock_request:
                mock_request.return_value = self.__response(
                    self.__json_bytes(response_json)
                )
                api_response = self.api.upload_file(body={'file': file1})
                self.__assert_request_called_with(
                    mock_request,
                    'http://petstore.swagger.io:80/v2/fake/uploadFile',
                    fields=(
                        api_client.RequestField(
                            name='file',
                            data=file_bytes,
                            filename=file_name,
                            headers={'Content-Type': 'application/octet-stream'}
                        ),
                    ),
                    content_type='multipart/form-data'
                )
                self.assertEqual(api_response.body, response_json)
        except petstore_api.ApiException as e:
            self.fail("upload_file() raised {0} unexpectedly".format(type(e)))
        finally:
            file1.close()

        # sending just bytes works also
        with patch.object(RESTClientObject, 'request') as mock_request:
            mock_request.return_value = self.__response(
                self.__json_bytes(response_json)
            )
            api_response = self.api.upload_file(body={'file': file_bytes})
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/uploadFile',
                fields=(
                    api_client.RequestField(
                        name='file',
                        data=file_bytes,
                        headers={'Content-Type': 'application/octet-stream'}
                    ),
                ),
                content_type='multipart/form-data'
            )
            self.assertEqual(api_response.body, response_json)

        # passing in an array of files to when file only allows one
        # raises an exceptions
        try:
            file = open(file_path1, "rb")
            with self.assertRaises(petstore_api.ApiTypeError):
                self.api.upload_file(body={'file': [file]})
        finally:
            file.close()

        # passing in a closed file raises an exception
        with self.assertRaises(ValueError):
            file = open(file_path1, "rb")
            file.close()
            self.api.upload_file(body={'file': file})

    def test_upload_files(self):
        """Test case for upload_files
        uploads files using multipart/form-data  # noqa: E501
        """
        import os
        test_file_dir = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "..", "testfiles"))
        file_name = '1px_pic1.png'
        file_path1 = os.path.join(test_file_dir, file_name)

        with open(file_path1, "rb") as some_file:
            file_bytes = some_file.read()
        file1 = open(file_path1, "rb")
        response_json = {
            'code': 200,
            'type': 'blah',
            'message': 'file upload succeeded'
        }
        try:
            with patch.object(RESTClientObject, 'request') as mock_request:
                mock_request.return_value = self.__response(
                    self.__json_bytes(response_json)
                )
                api_response = self.api.upload_files(body={'files': [file1, file1]})
                self.__assert_request_called_with(
                    mock_request,
                    'http://petstore.swagger.io:80/v2/fake/uploadFiles',
                    fields=(
                        api_client.RequestField(
                            name='files',
                            data=file_bytes,
                            filename=file_name,
                            headers={'Content-Type': 'application/octet-stream'}
                        ),
                        api_client.RequestField(
                            name='files',
                            data=file_bytes,
                            filename=file_name,
                            headers={'Content-Type': 'application/octet-stream'}
                        ),
                    ),
                    content_type='multipart/form-data'
                )
                self.assertEqual(api_response.body, response_json)
        except petstore_api.ApiException as e:
            self.fail("upload_file() raised {0} unexpectedly".format(type(e)))
        finally:
            file1.close()

        # sending just bytes works also
        with patch.object(RESTClientObject, 'request') as mock_request:
            mock_request.return_value = self.__response(
                self.__json_bytes(response_json)
            )
            api_response = self.api.upload_files(body={'files': [file_bytes, file_bytes]})
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/uploadFiles',
                fields=(
                    api_client.RequestField(
                        name='files',
                        data=file_bytes,
                        headers={'Content-Type': 'application/octet-stream'}
                    ),
                    api_client.RequestField(
                        name='files',
                        data=file_bytes,
                        headers={'Content-Type': 'application/octet-stream'}
                    ),
                ),
                content_type='multipart/form-data'
            )
            self.assertEqual(api_response.body, response_json)

    @staticmethod
    def __encode_multipart_formdata(fields: typing.Dict[str, typing.Any]) -> multipart.MIMEMultipart:
        m = multipart.MIMEMultipart("form-data")

        for field, value in fields.items():
            data = MIMEFormdata(field, "text", "plain")
            # data.set_payload(value, charset='us-ascii')
            data.set_payload(value)
            m.attach(data)

        return m

    # comment out below for the time being after adding better inline model support
    # ref: https://github.com/OpenAPITools/openapi-generator/pull/12104
    #
    #@patch.object(RESTClientObject, 'request')
    #def test_inline_composition(self, mock_request):
    #    """Test case for inline_composition

    #    testing composed schemas at inline locations  # noqa: E501
    #    """
    #    single_char_str = 'a'
    #    json_bytes = self.__json_bytes(single_char_str)

    #    # tx and rx json with composition at root level of schema for request + response body
    #    content_type = 'application/json'
    #    mock_request.return_value = self.__response(
    #        json_bytes
    #    )
    #    api_response = self.api.inline_composition(
    #        body=single_char_str,
    #        query_params={
    #            'compositionAtRoot': single_char_str,
    #            'compositionInProperty': {'someProp': single_char_str}
    #        },
    #        accept_content_types=(content_type,)
    #    )
    #    self.__assert_request_called_with(
    #        mock_request,
    #        'http://petstore.swagger.io:80/v2/fake/inlineComposition/',
    #        accept_content_type=content_type,
    #        content_type=content_type,
    #        query_params=(('compositionAtRoot', 'a'), ('someProp', 'a')),
    #        body=json_bytes
    #    )
    #    self.assertEqual(api_response.body, single_char_str)
    #    self.assertTrue(isinstance(api_response.body, schemas.StrSchema))

    #    # tx and rx json with composition at property level of schema for request + response body
    #    content_type = 'multipart/form-data'
    #    multipart_response = self.__encode_multipart_formdata(fields={'someProp': single_char_str})
    #    mock_request.return_value = self.__response(
    #        bytes(multipart_response),
    #        content_type=multipart_response.get_content_type()
    #    )
    #    api_response = self.api.inline_composition(
    #        body={'someProp': single_char_str},
    #        query_params={
    #            'compositionAtRoot': single_char_str,
    #            'compositionInProperty': {'someProp': single_char_str}
    #        },
    #        content_type=content_type,
    #        accept_content_types=(content_type,)
    #    )
    #    self.__assert_request_called_with(
    #        mock_request,
    #        'http://petstore.swagger.io:80/v2/fake/inlineComposition/',
    #        accept_content_type=content_type,
    #        content_type=content_type,
    #        query_params=(('compositionAtRoot', 'a'), ('someProp', 'a')),
    #        fields=(
    #            api_client.RequestField(
    #                name='someProp',
    #                data=single_char_str,
    #                headers={'Content-Type': 'text/plain'}
    #            ),
    #        ),
    #    )
    #    self.assertEqual(api_response.body, {'someProp': single_char_str})
    #    self.assertTrue(isinstance(api_response.body.someProp, schemas.StrSchema))

    #    # error thrown when a str is input which doesn't meet the composed schema length constraint
    #    invalid_value = ''
    #    variable_locations = 4
    #    for invalid_index in range(variable_locations):
    #        values = [single_char_str]*variable_locations
    #        values[invalid_index] = invalid_value
    #        with self.assertRaises(exceptions.ApiValueError):
    #            multipart_response = self.__encode_multipart_formdata(fields={'someProp': values[0]})
    #            mock_request.return_value = self.__response(
    #                bytes(multipart_response),
    #                content_type=multipart_response.get_content_type()
    #            )
    #            self.api.inline_composition(
    #                body={'someProp': values[1]},
    #                query_params={
    #                    'compositionAtRoot': values[2],
    #                    'compositionInProperty': {'someProp': values[3]}
    #                },
    #                content_type=content_type,
    #                accept_content_types=(content_type,)
    #            )

    def test_json_with_charset(self):
        # serialization + deserialization of json with charset works
        with patch.object(RESTClientObject, 'request') as mock_request:
            body = None
            content_type_with_charset = 'application/json; charset=utf-8'
            mock_request.return_value = self.__response(
                self.__json_bytes(body),
                content_type=content_type_with_charset
            )

            api_response = self.api.json_with_charset(body=body)
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/jsonWithCharset',
                body=self.__json_bytes(body),
                content_type=content_type_with_charset,
                accept_content_type=content_type_with_charset
            )

            assert isinstance(api_response.body, schemas.AnyTypeSchema)
            assert isinstance(api_response.body, schemas.NoneClass)
            assert api_response.body.is_none()

    def test_response_without_schema(self):
        # received response is not loaded into body because there is no deserialization schema defined
        with patch.object(RESTClientObject, 'request') as mock_request:
            body = None
            content_type = 'application/json'
            mock_request.return_value = self.__response(
                self.__json_bytes(body),
            )

            api_response = self.api.response_without_schema()
            self.__assert_request_called_with(
                mock_request,
                'http://petstore.swagger.io:80/v2/fake/responseWithoutSchema',
                method='GET',
                accept_content_type='application/json, application/xml',
                content_type=None
            )

            assert isinstance(api_response.body, schemas.Unset)


        with patch.object(RESTClientObject, 'request') as mock_request:
            mock_request.return_value = self.__response(
                'blah',
                content_type='text/plain'
            )

            # when an incorrect content-type is sent back, and exception is raised
            with self.assertRaises(exceptions.ApiValueError):
                self.api.response_without_schema()


if __name__ == '__main__':
    unittest.main()
