class Visuals:

    def __init__(self):
        pass

    def show_image(self, data, index=None, rows=2, cols=3):
        if (isinstance(index, int)):
            return self.plt.imshow(data[index])

        if (isinstance(index, list)):
            fig, axes = self.plt.subplots(1, len(index), figsize=(9, 5))
            for i, item in enumerate(index):
                axes[i].imshow(data[item])
            return None

        self.plt.figure(figsize=(18, 9))
        for i in range(rows*cols):
            ax = plt.subplot(rows, cols, i + 1)
            plt.imshow(data[i, :, :])
            plt.axis("off")

    def show_performance_curve(self, training_result, metric):

        train_perf = training_result.history[str(metric)]
        validation_perf = training_result.history['val_'+str(metric)]

        self.plt.plot(train_perf, label=metric)
        self.plt.plot(validation_perf, label='val_'+str(metric))

        self.plt.xlabel('Epoch')
        self.plt.ylabel(metric)
        self.plt.legend(loc='lower right')



    def plot_results(self, metrics, title=None, ylabel=None, ylim=None, metric_name=None, color=None):

        fig, ax = self.plt.subplots(figsize=(15, 4))

        if not (isinstance(metric_name, list) or isinstance(metric_name, tuple)):
            metrics = [metrics,]
            metric_name = [metric_name,]

        for idx, metric in enumerate(metrics):
            ax.plot(metric, color=color[idx])

            self.plt.xlabel("Epoch")
            self.plt.ylabel(ylabel)
            self.plt.title(title)
            self.plt.xlim([0, 3-1])
            self.plt.ylim(ylim)
    # Tailor x-axis tick marks
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        self.plt.grid(True)
        self.plt.legend(metric_name)
        self.plt.show()
        self.plt.close()


     def confusion_matrix(self, test_predictions, test_labels):
        test_predicted_labels = np.argmax(test_predictions, axis=1)

        test_true_labels = np.argmax(test_labels, axis=1)

        cm = confusion_matrix(test_true_labels, test_predicted_labels)

        cmd = ConfusionMatrixDisplay(confusion_matrix=cm)

        cmd.plot(include_values=True, cmap='viridis',
                 ax=None, xticks_rotation='horizontal')
        self.plt.show()
