from tensorflow.keras.layers import Layer, MultiHeadAttention, Dense, Dropout, LayerNormalization
import tensorflow as tf

class FeedForwardLayer(Layer):
    def __init__(self, d_model: int, d_ff: int, dropout_rate: float = 0.1):
        super(FeedForwardLayer, self).__init__()
        self.linear1 = Dense(d_ff, activation='relu')
        self.dropout = Dropout(dropout_rate)
        self.linear2 = Dense(d_model)

    def call(self, inputs: tf.Tensor, training: bool = False) -> tf.Tensor:
        x = self.linear1(inputs)
        x = self.dropout(x, training=training)
        return self.linear2(x)

class CustomMultiHeadAttention(MultiHeadAttention):
    def __init__(self, num_heads: int, key_dim: int, dropout_rate: float = 0.1):
        super(CustomMultiHeadAttention, self).__init__(num_heads=num_heads, key_dim=key_dim, dropout=dropout_rate)

    def call(self, query: tf.Tensor, value: tf.Tensor, key: tf.Tensor = None, attention_mask: tf.Tensor = None, training: bool = False) -> tf.Tensor:
        return super().call(query, value, key, attention_mask, training=training)

class EncoderLayer(Layer):
    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout_rate: float = 0.1):
        super(EncoderLayer, self).__init__()
        self.attention = CustomMultiHeadAttention(num_heads=num_heads, key_dim=d_model // num_heads, dropout_rate=dropout_rate)
        self.ffn = FeedForwardLayer(d_model, d_ff, dropout_rate)
        self.layernorm1 = LayerNormalization(epsilon=1e-6)
        self.layernorm2 = LayerNormalization(epsilon=1e-6)
        self.dropout1 = Dropout(dropout_rate)
        self.dropout2 = Dropout(dropout_rate)

    def call(self, inputs: tf.Tensor, training: bool = False) -> tf.Tensor:
        attn_output = self.attention(inputs, inputs, training=training)
        out1 = self.layernorm1(inputs + self.dropout1(attn_output, training=training))
        ffn_output = self.ffn(out1, training=training)
        return self.layernorm2(out1 + self.dropout2(ffn_output, training=training))

class DecoderLayer(Layer):
    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout_rate: float = 0.1):
        super(DecoderLayer, self).__init__()
        self.attention1 = CustomMultiHeadAttention(num_heads=num_heads, key_dim=d_model // num_heads, dropout_rate=dropout_rate)
        self.attention2 = CustomMultiHeadAttention(num_heads=num_heads, key_dim=d_model // num_heads, dropout_rate=dropout_rate)
        self.ffn = FeedForwardLayer(d_model, d_ff, dropout_rate)
        self.layernorm1 = LayerNormalization(epsilon=1e-6)
        self.layernorm2 = LayerNormalization(epsilon=1e-6)
        self.layernorm3 = LayerNormalization(epsilon=1e-6)
        self.dropout1 = Dropout(dropout_rate)
        self.dropout2 = Dropout(dropout_rate)
        self.dropout3 = Dropout(dropout_rate)

    def call(self, inputs: tf.Tensor, enc_output: tf.Tensor, training: bool = False) -> tf.Tensor:
        attn1 = self.attention1(inputs, inputs, training=training)
        out1 = self.layernorm1(inputs + self.dropout1(attn1, training=training))
        attn2 = self.attention2(enc_output, enc_output, out1, training=training)
        out2 = self.layernorm2(out1 + self.dropout2(attn2, training=training))
        ffn_output = self.ffn(out2, training=training)
        return self.layernorm3(out2 + self.dropout3(ffn_output, training=training))