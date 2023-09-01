from block_local_self_attention import *
torch.manual_seed(0)
import random
random.seed(0)

# batch, num_heads, sequence length, hidden_size
n, h, t, d = 2, 4, 58, 32  

Q, K, V = torch.randn(n, h, t, d), torch.randn(n, h, t, d), torch.randn(n, h, t, d)
attention_mask = torch.zeros(n, 1, 1, t).float()

attn = BlockLocalSelfAttention(block_size=16, compute_global_attention=True, is_causal=False, attention_dropout_prob=0.0)

# expect (n, h, t, d) inputs,
# attention_mask is (n, 1, 1, t) or (n, 1, t, t) for causal
# attention_mask is 0 for no mask, -inf for mask (similar to most HuggingFace models)
outputs = attn(Q, K, V, attention_mask)

print(outputs.shape)
print(outputs[1,:4,1,1])

# batch, num_heads, sequence length, hidden_size
n, h, t, d = 2, 4, 83, 32  

Q, K, V = torch.randn(n, h, t, d), torch.randn(n, h, t, d), torch.randn(n, h, t, d)
attention_mask = torch.zeros(n, 1, 1, t).float()

attn = BlockLocalSelfAttention(block_size=8, compute_global_attention=False, is_causal=False, attention_dropout_prob=0.0)

# expect (n, h, t, d) inputs,
# attention_mask is (n, 1, 1, t) or (n, 1, t, t) for causal
# attention_mask is 0 for no mask, -inf for mask (similar to most HuggingFace models)
outputs = attn(Q, K, V, attention_mask)

print(outputs.shape)
print(outputs[1,:4,1,1])

# batch, num_heads, sequence length, hidden_size
n, h, t, d = 2, 4, 83, 32  

Q, K, V = torch.randn(n, h, t, d), torch.randn(n, h, t, d), torch.randn(n, h, t, d)
attention_mask = torch.zeros(n, 1, 1, t).float()

attn = BlockLocalSelfAttention(block_size=8, compute_global_attention=True, is_causal=True, attention_dropout_prob=0.0)

# expect (n, h, t, d) inputs,
# attention_mask is (n, 1, 1, t) or (n, 1, t, t) for causal
# attention_mask is 0 for no mask, -inf for mask (similar to most HuggingFace models)
outputs = attn(Q, K, V, attention_mask)

print(outputs.shape)
print(outputs[1,:4,1,1])