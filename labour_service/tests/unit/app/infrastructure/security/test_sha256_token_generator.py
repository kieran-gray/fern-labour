from app.labour.infrastructure.security.sha256_token_generator import SHA256TokenGenerator


def test_can_generate_token() -> None:
    input = "input"
    generator = SHA256TokenGenerator("salt")
    token = generator.generate(input)
    assert token != input


def test_can_validate_token() -> None:
    input = "input"
    generator = SHA256TokenGenerator("salt")
    token = generator.generate(input)
    assert generator.validate(input, token)


def test_validation_fails_for_invalid_token() -> None:
    input = "input"
    generator = SHA256TokenGenerator("salt")
    token = generator.generate(input)
    assert not generator.validate("not the input", token)


def test_validation_fails_for_generator_with_different_salt() -> None:
    input = "input"
    generator = SHA256TokenGenerator("salt")
    token = generator.generate(input)

    generator = SHA256TokenGenerator("different_salt")
    assert not generator.validate(input, token)
