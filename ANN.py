import numpy


def sigmoid(inpt):
    return 1.0 / (1.0 + numpy.exp(-1 * inpt))


def predict_outputs(w1, w2, data_inputs, out):
    r1 = data_inputs
    r1 = numpy.matmul(r1, w1)
    r1 = sigmoid(r1)
    a = []
    for i, data in enumerate(w2):
        for j in range(len(data)):
            a.append(w2[i][j])

    newlist = []
    for i in range(10):
        newlist.append([])
        for j in range(out):
            newlist[i].append(a[i*out+j])

    r2 = numpy.matmul(r1, newlist)
    output = sigmoid(r2)
    predicted_label = numpy.where(output == numpy.max(output))[0][0]
    return predicted_label

