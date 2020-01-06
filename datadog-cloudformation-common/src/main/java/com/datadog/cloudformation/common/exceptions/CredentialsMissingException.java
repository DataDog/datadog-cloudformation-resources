// Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
// This product includes software developed at Datadog (https://www.datadoghq.com/).
// Copyright 2019-Present Datadog, Inc.
package com.datadog.cloudformation.common.exceptions;

public class CredentialsMissingException extends Exception {
    public CredentialsMissingException() { super(); }
    public CredentialsMissingException(String message) { super(message); }
    public CredentialsMissingException(String message, Throwable cause) { super(message, cause); }
    public CredentialsMissingException(Throwable cause) { super(cause); }
  }
