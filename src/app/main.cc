#include <gtkmm.h>
#include <iostream>


class MainWindow {
  public:
    MainWindow();
    void run(int argc, char **argv);

  protected:
    Glib::RefPtr<Gtk::Application> app;
    Glib::RefPtr<Gtk::Builder> builder;
    Gtk::Window* window = nullptr;

    void openFile();
    void saveFile();
    void clear();
    void exit();
};

MainWindow::MainWindow() {
  app = Gtk::Application::create("org.breta.diakritik");
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

  // Menu
  Gtk::ImageMenuItem* button = nullptr;
  builder->get_widget("exit_button", button);
  button->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::exit));

  builder->get_widget("window", window);
}

void MainWindow::exit() {
  delete window;
}

void MainWindow::run(int argc, char **argv) {
  app->run(*window, argc, argv);
}

// static void on_button_clicked() {
//   if(pDialog)

// }

int main (int argc, char **argv) {
  MainWindow window;
  window.run(argc, argv);
  // if(pDialog) {
  //   //Get the GtkBuilder-instantiated Button, and connect a signal handler:
  //   Gtk::Button* pButton = nullptr;
  //   builder->get_widget("quit_button", pButton);
  //   if(pButton) {
  //     pButton->signal_clicked().connect( sigc::ptr_fun(on_button_clicked) );
  //   }
  // }

  return 0;
}
