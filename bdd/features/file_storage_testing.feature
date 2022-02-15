Feature: Testing POST method
  Before test should setup environment: download files for test from cloud
  Raise POST requests using 'requests' library
  Validate HTTP response code and parse JSON response
  Make sure to run FileStorage server as pre-condition


  Background:
    Given Set api endpoint as "upload"
#    And Set the path to default folder for upload files to server as "tests/files_for_upload/"
#    And Set the responses base keys as "id, name, tag, size, mimeType, modificationTime"
#    And Set which files should be upload as "test1.docx, test2.xlsx, test3.txt, test4.pdf, test5.jpg"
#    And Set link to zip_archive or files for test in the cloud as "https://disk.yandex.ru/d/aJoFOPqLRHGGXw"

  Scenario Outline: testing POST method with empty data
    When Set file "<file_name>" as body
    Then Raise "POST" HTTP request
    And Response content should be JSON format
    And Response http code should be 201
    And Response content should have base keys "id, name, tag, size, mimeType, modificationTime"

    Examples: File names
      | file_name  |
      | test1.docx |
      | test2.xlsx |
      | test3.txt  |
      | test4.pdf  |
      | test5.jpg  |


  Scenario Outline: testing POST method with given file id
    When Set "file id" as "<sending_id>"
    And Set file "test1.docx" as body
    Then Raise "POST" HTTP request
    And Response http code should be 201
    And Response content should be JSON format
    And Response content should have base keys "id, name, tag, size, mimeType, modificationTime"
    And Response content "id" should be "<expected_id>"

    Examples: file id
      | sending_id | expected_id |
      | 5          | 5           |
      | 15         | 15          |
      | 2          | 2           |
      | 2          | 2           |


  Scenario Outline: testing POST method with given content type
    When Set "content type" as "<content type>"
    And Set file "<file_name>" as body
    Then Raise "POST" HTTP request
    And Response content should be JSON format
    And Response http code should be 201
    And Response content should have base keys "id, name, tag, size, mimeType, modificationTime"
    And Response content "mimeType" should be "<content type>"

    Examples: Set content type for each file
      | file_name  | content type                                                            |
      | test1.docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document |
      | test2.xlsx | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet       |
      | test3.txt  | text/plain                                                              |
      | test4.pdf  | application/pdf                                                         |
      | test5.jpg  | image/jpeg                                                              |
      | test1.docx | test_content_type                                                       |


  Scenario Outline: testing POST method with given name
    When Set "name" as "<test_name>"
    And Set file "test1.docx" as body
    Then Raise "POST" HTTP request
    And Response content should be JSON format
    And Response http code should be 201
    And Response content should have base keys "id, name, tag, size, mimeType, modificationTime"
    And Response content "name" should be "<test_name>"
    Examples: File names
      | test_name |
      | name1     |
      | foo       |
      | bar       |
      | 1234      |

