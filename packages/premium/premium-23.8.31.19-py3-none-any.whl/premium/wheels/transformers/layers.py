#!/user/bin/env python3
import torch
import torch.nn.functional as F
from torch import Tensor, nn
from transformers import AutoConfig

# refer
# https://medium.com/the-dl/transformers-from-scratch-in-pytorch-8777e346ca51


def scaled_dot_product_attention(query: Tensor, key: Tensor,
                                 value: Tensor) -> Tensor:
    """
    query = torch.randn(2, 3, 4)
    key = torch.randn(2, 3, 4)
    value = torch.randn(2, 3, 4)
    atten = scaled_dot_product_attention(query, key, value)
    print(atten)
    print(atten.shape)
    """
    temp = query.bmm(key.transpose(1, 2))
    scale = query.size(-1)**0.5
    softmax = F.softmax(temp / scale, dim=-1)
    return softmax.bmm(value)


class AttentionHead(nn.Module):

    def __init__(self, dim_in: int, dim_k: int, dim_v: int):
        super().__init__()
        self.q = nn.Linear(dim_in, dim_k)
        self.k = nn.Linear(dim_in, dim_k)
        self.v = nn.Linear(dim_in, dim_v)

    def forward(self, hidden_state: Tensor) -> Tensor:
        """
        hidden_state shape: batch_size * seq_len * dim_in(feature number)
        return shape: dim_in * dim_v
        """
        return scaled_dot_product_attention(self.q(hidden_state),
                                            self.k(hidden_state),
                                            self.v(hidden_state))


class MultiHeadAttention(nn.Module):

    def __init__(self, num_heads: int, dim_in: int, dim_k: int,
                 dim_v: int) -> None:
        super().__init__()
        self.heads = nn.ModuleList(
            [AttentionHead(dim_in, dim_k, dim_v) for _ in range(num_heads)])
        # num_heads * dim_v is the hidden size of the transformer
        self.linear = nn.Linear(num_heads * dim_v, dim_in)

    def forward(self, hidden_state: Tensor) -> Tensor:
        return self.linear(
            torch.cat([h(hidden_state) for h in self.heads], dim=-1))


class PositionwiseFeedforward(nn.Module):

    def __init__(self, dim_in: int, dim_hidden: int) -> None:
        super().__init__()
        self.linear1 = nn.Linear(dim_in, dim_hidden)
        self.linear2 = nn.Linear(dim_hidden, dim_in)
        self.gelu = nn.GELU()
        self.dropout = nn.Dropout(0.1)

    def forward(self, x: Tensor) -> Tensor:
        x = self.gelu(self.linear1(x))
        x = self.linear2(x)
        return self.dropout(x)


class TransformerEncoderLayer(nn.Module):

    def __init__(self, dim_in: int, dim_k: int, dim_v: int, num_heads: int,
                 dim_hidden: int) -> None:
        super().__init__()
        self.attention = MultiHeadAttention(num_heads, dim_in, dim_k, dim_v)
        self.norm1 = nn.LayerNorm(dim_in)
        self.norm2 = nn.LayerNorm(dim_in)
        self.feedforward = PositionwiseFeedforward(dim_in, dim_hidden)

    def forward(self, x: Tensor) -> Tensor:
        hidden_state = self.norm1(x)
        x = x + self.attention(hidden_state)
        x = x + self.feedforward(self.norm2(x))
        return x



if __name__ == '__main__':
    model = 'bert-base-uncased'
    config = AutoConfig.from_pretrained(model)
    print(config)
