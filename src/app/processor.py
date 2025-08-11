"""Processor module for stock-backtest-meanreversion signal generation.

Validates input messages and detects mean reversion signals using
deviation from moving average.
"""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import ValidatedMessage
from app.utils.validate_data import validate_message_schema

logger = setup_logger(__name__)


def validate_input_message(message: dict[str, Any]) -> ValidatedMessage:
    """Validate the incoming raw message against the expected schema.

    Args:
        message (dict[str, Any]): Raw input message.

    Returns:
        ValidatedMessage: A validated message object.

    Raises:
        ValueError: If the message format is invalid.

    """
    logger.debug("🔍 Validating message schema...")
    if not validate_message_schema(message):
        logger.error("❌ Invalid message schema: %s", message)
        raise ValueError("Invalid message format")
    return message  # type: ignore[return-value]


def compute_meanreversion_signal(message: ValidatedMessage) -> dict[str, Any]:
    """Detect mean reversion signals using price vs. moving average.

    Args:
        message (ValidatedMessage): The validated input data.

    Returns:
        dict[str, Any]: Enriched message with mean reversion signal.

    """
    symbol = message.get("symbol", "UNKNOWN")
    price = float(message.get("price", 100.0))
    moving_avg = float(message.get("moving_average", 100.0))

    logger.info("↩️ Computing mean reversion signal for %s", symbol)

    deviation = (price - moving_avg) / moving_avg
    signal = (
        "REVERT_UP" if deviation < -0.03 else ("REVERT_DOWN" if deviation > 0.03 else "NEUTRAL")
    )

    result = {
        "mean_reversion_deviation": round(deviation, 4),
        "mean_reversion_signal": signal,
    }

    logger.debug("📉 Mean reversion result for %s: %s", symbol, result)
    return {**message, **result}
