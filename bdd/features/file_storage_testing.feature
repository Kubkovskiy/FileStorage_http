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

  Scenario: testing POST method with empty data
    When Set file "test1.docx" as body
    Then Raise "POST" HTTP request
    And Response content should be JSON format
    And Response http code should be 201
    And Response content should have base keys "id, name, tag, size, mimeType, modificationTime"

  Scenario: testing POST method with current file id
    When Set "file id" as "23"
    And Set file "test1.docx" as body
    Then Raise "POST" HTTP request
    And Response http code should be 201
    And Response content should be JSON format
    And Response content should have base keys "id, name, tag, size, mimeType, modificationTime"
    And Response content "id" should be "23"

  Scenario: testing POST method with current content type

    When Set "content type" as "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    And Set file "test1.docx" as body
    Then Raise "POST" HTTP request
    And Response content should be JSON format
    And Response http code should be 201
    And Response content should have base keys "id, name, tag, size, mimeType, modificationTime"
    And Response content "mimeType" should be "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

  Scenario: testing POST method with current name
    When Set "name" as "test_name"
    And Set file "test1.docx" as body
    Then Raise "POST" HTTP request
    And Response content should be JSON format
    And Response http code should be 201
    And Response content should have base keys "id, name, tag, size, mimeType, modificationTime"
    And Response content "name" should be "test_name"
