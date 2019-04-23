#include <gtkmm.h>
#include <iostream>


class MainWindow {
  public:
    MainWindow();
    void run(int argc, char **argv) {
      app->run(*window, argc, argv);
    };

  protected:
    Glib::RefPtr<Gtk::Application> app;
    Glib::RefPtr<Gtk::Builder> builder;
    Glib::RefPtr<Gtk::TextBuffer> buffer;
    Glib::RefPtr<Gtk::Clipboard> clipboard;

    Gtk::ApplicationWindow* window = nullptr;
    Gtk::AboutDialog* aboutDialog = nullptr;
    Gtk::TextView* textView = nullptr;

    void openFile();
    void saveFile();
    void clear();
    void copyAll( );
    void about();
    void paste() { textView->get_buffer()->paste_clipboard(clipboard); }
    void exit() { window->close(); }
};


MainWindow::MainWindow() {
  app = Gtk::Application::create("com.bretahajek.diakritik");
  clipboard = Gtk::Clipboard::get();

  builder = Gtk::Builder::create();
  try {
    builder->add_from_file("main.glade");
  } catch(const Glib::FileError& ex) {
    std::cerr << "FileError: " << ex.what() << std::endl;
  } catch(const Glib::MarkupError& ex) {
    std::cerr << "MarkupError: " << ex.what() << std::endl;
  } catch(const Gtk::BuilderError& ex) {
    std::cerr << "BuilderError: " << ex.what() << std::endl;
  }

  // Widgets
  builder->get_widget("about_dialog", aboutDialog);
  builder->get_widget("text_view", textView);
  builder->get_widget("window", window);

  // Menu
  Gtk::ImageMenuItem* button = nullptr;
  builder->get_widget("exit_button", button);
  button->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::exit));
  builder->get_widget("about_button", button);
  button->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::about));
  builder->get_widget("paste_button", button);
  button->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::paste));
}

void MainWindow::about() {
  if (aboutDialog) {
    aboutDialog->run();
    aboutDialog->close();
  }
}


int main (int argc, char **argv) {
  MainWindow window;
  window.run(argc, argv);


  return 0;
}
