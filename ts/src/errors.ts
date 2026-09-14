/** Custom error types for Instagram and Threads operations */

export class InstagramError extends Error {
  public readonly statusCode?: number;
  public readonly raw?: any;

  constructor(message: string, statusCode?: number, raw?: any) {
    super(message);
    this.name = "InstagramError";
    this.statusCode = statusCode;
    this.raw = raw;
  }
}

export class AuthError extends InstagramError {
  constructor(message: string = "Instagram authentication failed or session expired", raw?: any) {
    super(message, 401, raw);
    this.name = "AuthError";
  }
}

export class ChallengeRequiredError extends InstagramError {
  public readonly challengeUrl?: string;

  constructor(message: string = "Checkpoint challenge required by Instagram", challengeUrl?: string, raw?: any) {
    super(message, 400, raw);
    this.name = "ChallengeRequiredError";
    this.challengeUrl = challengeUrl;
  }
}

export class RateLimitError extends InstagramError {
  constructor(message: string = "Instagram rate limit (429) encountered", raw?: any) {
    super(message, 429, raw);
    this.name = "RateLimitError";
  }
}

export class InvalidRequestError extends InstagramError {
  constructor(message: string = "Invalid request payload or malformed parameter", raw?: any) {
    super(message, 400, raw);
    this.name = "InvalidRequestError";
  }
}

export class ServerError extends InstagramError {
  constructor(message: string = "Instagram internal server error (5xx)", statusCode: number = 500, raw?: any) {
    super(message, statusCode, raw);
    this.name = "ServerError";
  }
}
