# Errort Documentation
- **Title:** Error Documentation
- **Course:** NEU CS5500 Fall 2023
- **Date:** Dec 7, 2023
- **Author:** Yiwen Wang, Xinyi Gao, Yijia Ma
- **Version:** 2.0
- **Contents:** Document error status codes and meanings

**Revision History**
|Date|Version|Description|Author|
|:----:|:----:|:----:|:----:|
|Nov 9, 2023|1.0|Initial release| Yiwen Wang|
|Dec 7, 2023|2.0|Update API| Yiwen Wang|

## Overview
This document describes the error handling approach in the API, including common error codes and their meanings.

### Common Errors
- **401 Unauthorized**: Authentication failed or token is invalid.
- **404 Not Found**: The requested resource was not found.
- **500 Internal Server Error**: General server errors.

### Error Handling in Code
Errors are managed using HTTP