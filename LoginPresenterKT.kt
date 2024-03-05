import com.example.demo.LoginPresenter
import com.example.demo.LoginView
import io.mockk.*
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.runBlockingTest
import org.junit.After
import org.junit.Before
import org.junit.Test

@ExperimentalCoroutinesApi
class LoginPresenterTest {

    private lateinit var presenter: LoginPresenter
    private val view: LoginView = mockk()

    @Before
    fun setup() {
        presenter = LoginPresenter(view)
    }

    @After
    fun teardown() {
        clearAllMocks()
    }

    @Test
    fun `login success`() = runBlockingTest {
        coEvery { view.enableLogoutButton() } just Runs
        coEvery { view.disableLoginButton() } just Runs
        coEvery { view.enableOTPButton() } just Runs

        presenter.login("demo", "password")
 
        coVerify { view.enableLogoutButton() }
        coVerify { view.disableLoginButton() }
        coVerify { view.enableOTPButton() }
        coVerify(exactly = 0) { view.showErrorMessage(any()) }
    }

    @Test
    fun `login failure shows error message`() = runBlockingTest {
        coEvery { view.showErrorMessage(any()) } just Runs

        presenter.login("invalid", "password")

        coVerify { view.showErrorMessage("Login failed. Please check your credentials.") }
        coVerify(exactly = 0) { view.enableLogoutButton() }
        coVerify(exactly = 0) { view.disableLoginButton() }
        coVerify(exactly = 0) { view.enableOTPButton() }
    }

    @Test
    fun `logout`() = runBlockingTest {
        coEvery { view.disableLogoutButton() } just Runs
        coEvery { view.enableLoginButton() } just Runs
        coEvery { view.disableOTPButton() } just Runs

        presenter.logout()

        coVerify { view.disableLogoutButton() }
        coVerify { view.enableLoginButton() }
        coVerify { view.disableOTPButton() }
    }

    @Test
    fun `verifyOTP success`() = runBlockingTest {
        coEvery { view.enableLogoutButton() } just Runs
        coEvery { view.disableOTPButton() } just Runs

        presenter.verifyOTP("123456")

        coVerify { view.enableLogoutButton() }
        coVerify { view.disableOTPButton() }
        coVerify(exactly = 0) { view.showErrorMessage(any()) }
    }

    @Test
    fun `verifyOTP failure shows error message`() = runBlockingTest {
        coEvery { view.showErrorMessage(any()) } just Runs

        presenter.verifyOTP("654321")

        coVerify { view.showErrorMessage("OTP verification failed. Please try again.") }
        coVerify(exactly = 0) { view.enableLogoutButton() }
        coVerify(exactly = 0) { view.disableOTPButton() }
    }
}