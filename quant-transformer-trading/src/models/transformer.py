from tensorflow import keras
from tensorflow.keras import layers

class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.attention = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential([
            layers.Dense(ff_dim, activation='relu'),
            layers.Dense(embed_dim)
        ])
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.attention(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

class Transformer(keras.Model):
    def __init__(self, num_layers, embed_dim, num_heads, ff_dim, input_shape, rate=0.1):
        super(Transformer, self).__init__()
        self.encoder = [TransformerBlock(embed_dim, num_heads, ff_dim, rate) for _ in range(num_layers)]
        self.final_layer = layers.Dense(1)  # Output layer for regression

    def call(self, inputs, training):
        x = inputs
        for encoder in self.encoder:
            x = encoder(x, training)
        return self.final_layer(x)

def create_transformer_model(num_layers, embed_dim, num_heads, ff_dim, input_shape):
    inputs = layers.Input(shape=input_shape)
    transformer = Transformer(num_layers, embed_dim, num_heads, ff_dim, input_shape)
    outputs = transformer(inputs)
    model = keras.Model(inputs=inputs, outputs=outputs)
    return model