@fixtures.preparing_files_for_upload_and_delete_after_session
Feature: REST API Testing FileStorage
  Raise POST, GET, DELETE, DOWNLOAD requests using 'requests' library
  Validate HTTP response code and parse JSON response
  Make sure to run FileStorage server as pre-condition

  Background:
    Given Set base server url is "http://127.0.0.1:9000/api/"
      And Set the path to default folder for upload files to server is "tests/files_for_upload/"
      And Set the responses base keys is 'id', 'name', 'tag', 'size', 'mimeType', 'modificationTime'
#      And Set default file names which should test is 'test1.docx', 'test2.xlsx', 'test3.txt', 'test4.pdf', 'test5.jpg'
#      And Set link to test files in the cloud is "https://disk.yandex.ru/d/aJoFOPqLRHGGXw"


  Scenario: testing POST method with empty data
    Given for tests a = 2
    Then should return 6