package com.datadog.cloudformation.common.exceptions;

public class CredentialsMissingException extends Exception {
    public CredentialsMissingException() { super(); }
    public CredentialsMissingException(String message) { super(message); }
    public CredentialsMissingException(String message, Throwable cause) { super(message, cause); }
    public CredentialsMissingException(Throwable cause) { super(cause); }
  }