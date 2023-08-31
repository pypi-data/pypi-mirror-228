import torch
import torch.nn as nn


class ParallelConv(nn.Module):
    def __init__(self, input_dims, filters, dropout=0.5):
        super().__init__()
        convs = []
        self.output_dims = sum([t[1] for t in filters])
        for (filter_length, output_dims) in filters:
            pad = filter_length//2
            conv = nn.Sequential(
                nn.Conv1d(input_dims, output_dims, filter_length, padding=pad),
                nn.ReLU()
            )
            convs.append(conv)
        # Add the module so its managed correctly
        self.convs = nn.ModuleList(convs)
        self.conv_drop = nn.Dropout(dropout)

    def forward(self, input_bct):
        mots = []
        for conv in self.convs:
            # In Conv1d, data BxCxT, max over time
            conv_out = conv(input_bct)
            mot, _ = conv_out.max(2)
            mots.append(mot)
        mots = torch.cat(mots, 1)
        return self.conv_drop(mots)


class ConvClassifier(nn.Module):
    def __init__(self, embeddings, num_classes, embed_dims,
                 filters=[(2, 100), (3, 100), (4, 100)],
                 dropout=0.5, hidden_units=[]):
        super().__init__()
        self.embeddings = embeddings
        self.dropout = nn.Dropout(dropout)
        self.convs = ParallelConv(embed_dims, filters, dropout)

        input_units = self.convs.output_dims
        output_units = self.convs.output_dims
        sequence = []
        for h in hidden_units:
            sequence.append(self.dropout(nn.Linear(input_units, h)))
            input_units = h
            output_units = h

        sequence.append(nn.Linear(output_units, num_classes))
        self.outputs = nn.Sequential(*sequence)

    def forward(self, inputs):
        one_hots, lengths = inputs
        embed = self.dropout(self.embeddings(one_hots))
        embed = embed.transpose(1, 2).contiguous()
        hidden = self.convs(embed)
        linear = self.outputs(hidden)
        return F.log_softmax(linear, dim=-1)
